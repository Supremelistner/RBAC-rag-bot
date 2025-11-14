
from langchain_huggingface import HuggingFaceEmbeddings

def get_embedder():
    print("[EMBED] Loading MiniLM embeddings...")
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
