import logging
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from Backend.Rag.rag_chain import RAGChain
from Backend.auth.routes import get_current_user_role as require_token  # returns {"username":..., "role":...}

router = APIRouter()

# Logger
logger = logging.getLogger("rag_api")
logger.setLevel(logging.DEBUG)

# -----------------------------
# Request Schema
# -----------------------------
class RAGQuery(BaseModel):
    question: str


# -----------------------------
# RAG ENDPOINT
# -----------------------------
@router.post("/rag/query")
def rag_query(payload: RAGQuery, user=Depends(require_token)):
    """
    Performs a RAG query using the user's role from the JWT token.
    """

    question = payload.question
    role = user.get("role")  # Extracted from JWT

    if not role:
        raise HTTPException(status_code=403, detail="User role missing")

    logger.info(f"[RAG-API] Query received | user_role={role} | question={question}")

    # -----------------------------
    # Initialize RAG Chain
    # -----------------------------
    try:
        chain = RAGChain(role)
    except Exception as e:
        logger.exception("[RAG-API] Failed to initialize RAGChain")
        raise HTTPException(status_code=500, detail="RAG initialization error")

    # -----------------------------
    # Run RAG inference
    # -----------------------------
    try:
        answer = chain.invoke(question)
    except Exception:
        logger.exception("[RAG-API] Error during RAG execution")
        raise HTTPException(status_code=500, detail="RAG execution failed")

    # -----------------------------
    # Collect Source Documents
    # -----------------------------
    try:
        docs = chain.retriever.invoke(question)
        sources = [
            {
                "source": d.metadata.get("source", "unknown"),
                "role": d.metadata.get("role", "unknown"),
                "content_snippet": d.page_content[:300],
            }
            for d in docs
        ]
    except Exception:
        sources = []

    # -----------------------------
    # Final Response
    # -----------------------------
    return {
        "role": role,
        "question": question,
        "answer": answer,
        "sources": sources
    }
