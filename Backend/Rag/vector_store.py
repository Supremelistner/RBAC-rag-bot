
import os
from langchain_chroma import Chroma

VECTOR_DIR = "./Backend/Rag/chroma_index"

def get_vectorstore(embeddings):
    print(f"[VECTOR] Initializing Chroma at {VECTOR_DIR}")
    os.makedirs(VECTOR_DIR, exist_ok=True)

    return Chroma(
        collection_name="company_docs",
        persist_directory=VECTOR_DIR,
        embedding_function=embeddings
    )
