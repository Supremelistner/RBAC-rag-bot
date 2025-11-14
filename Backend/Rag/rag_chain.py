# Backend/Rag/rag_chain.py
import os
import logging
from typing import List

from transformers import pipeline
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.runnables import RunnableMap

logger = logging.getLogger("rag_chain")
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler("rag_chain_debug.log")
fh.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logger.addHandler(fh)

VECTORSTORE_PATH = os.getenv("CHROMA_PERSIST_DIR", "./Backend/Rag/chroma_index")
EMBED_MODEL = os.getenv("EMBED_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
HF_LLM_MODEL = os.getenv("HF_LLM_MODEL", "google/flan-t5-base")

# maximum token-ish length we want to allow in LLM input; if context is larger we'll truncate by chars
# (Token counts depend on model/tokenizer; pick conservatively)
MAX_CONTEXT_CHARS = 3000


class RAGChain:
    def __init__(self, role: str, k: int = 4):
        """
        role: string like "Marketing"
        k: number of retrieved docs to include
        """
        print(f"[RAG] Building RAG chain for role={role}")
        self.role = role
        self.k = k

        # Embeddings
        logger.info("Loading embeddings")
        print("[RAG] Loading embeddings model…")
        self.embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL)
        print("[RAG] Embeddings loaded")
        logger.info("Embeddings loaded")

        # Vectorstore / Chroma
        print(f"[RAG] Loading Chroma DB from: {VECTORSTORE_PATH}")
        self.vectorstore = Chroma(
            persist_directory=VECTORSTORE_PATH,
            embedding_function=self.embeddings,
            collection_name="company_docs",
        )
        print("[RAG] Chroma loaded")
        logger.info("Chroma loaded")

        # Retriever with metadata filter
        print(f"[RAG] Creating retriever for role={role}")
        self.retriever = self.vectorstore.as_retriever(
            search_kwargs={
                "k": self.k,
                "filter": {"role": self.role},
            }
        )
        print("[RAG] Retriever created")
        logger.info("Retriever created")

        # HF LLM pipeline
        print(f"[RAG] Loading LLM: {HF_LLM_MODEL}")
        # device=-1 uses CPU; if you want to use GPU set device=0 (and ensure model fits)
        self.llm_pipeline = pipeline(
            "text2text-generation",
            model=HF_LLM_MODEL,
            max_length=512,  # generation max; keep reasonably small
            do_sample=False,
            device=-1,
        )
        print("[RAG] HF pipeline loaded successfully")
        logger.info("HF pipeline loaded")

        # System / template text (we will format into a single string)
        self.system_header = (
            "You are an assistant that MUST use ONLY the supplied Context to answer. "
            "If the answer does not appear in the Context, respond: \"I don't have enough information to answer that.\"\n\n"
            "Role: {role}\n\n"
            "Context:\n{context}\n\n"
            "Question: {question}\n\n"
            "Answer:"
        )

        print("[RAG] LCEL built (simple explicit flow)")

    def _build_prompt(self, docs: List, question: str) -> str:
        """
        Join docs into a single context string and return full prompt text.
        Truncates context if too long to avoid Transformer errors.
        """
        # docs are Document-like with page_content attribute
        pieces = []
        for d in docs:
            content = getattr(d, "page_content", None)
            if not content:
                continue
            # include a small marker and truncated snippet per doc to keep prompt smaller
            pieces.append(content.strip())

        context = "\n\n---\n\n".join(pieces).strip()
        if not context:
            context = "No context available."

        # If context too large, truncate (keep the end or start as you prefer)
        if len(context) > MAX_CONTEXT_CHARS:
            logger.warning("Context too long; truncating to %d chars", MAX_CONTEXT_CHARS)
            context = context[:MAX_CONTEXT_CHARS] + "\n\n[...context truncated...]"

        prompt = self.system_header.format(role=self.role, context=context, question=question)
        return prompt

    def invoke(self, question: str) -> str:
        """
        High-level call used by api.py. Returns the generated answer string.
        """
        try:
            # get relevant docs via retriever.invoke (LangChain retriever runnable)
            # retriever.invoke returns a list of Document objects
            docs = self.retriever.invoke(question)
        except Exception as e:
            # log and re-raise so api.py can catch
            logger.exception("Retriever invoke failed")
            raise

        # build final prompt string
        prompt_text = self._build_prompt(docs, question)

        # IMPORTANT: transformers pipeline expects str (or list[str])
        try:
            output = self.llm_pipeline(prompt_text, max_length=300)  # returns list of dicts
            if isinstance(output, list) and len(output) > 0:
                # different HF versions use different keys: prefer generated_text then text
                first = output[0]
                answer = first.get("generated_text") or first.get("text") or str(first)
            else:
                answer = ""
        except Exception:
            logger.exception("LLM pipeline call failed")
            raise

        return answer
