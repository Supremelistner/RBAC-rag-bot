# Backend/Rag/rag_ingest.py

from Backend.Rag.loader import load_documents
from Backend.Rag.embedder import get_embedder
from Backend.Rag.vector_store import get_vectorstore

def ingest_documents():
    print("🚀 Starting ingestion...")

    docs = load_documents("./data")
    print(f"Loaded {len(docs)} chunked docs.")

    embeddings = get_embedder()
    vectorstore = get_vectorstore(embeddings)

    print("Adding documents to ChromaDB...")
    vectorstore.add_documents(docs)

    print("✅ Ingestion completed!")

if __name__ == "__main__":
    ingest_documents()
