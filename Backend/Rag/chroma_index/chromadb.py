from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

emb = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

db = Chroma(
    persist_directory="./Backend/Rag/chroma_index",
    embedding_function=emb,
    collection_name="company_docs"
)

print("Total documents:", db._collection.count())

docs = db._collection.get(include=["metadatas", "documents"])

for i in range(len(docs["ids"])):
    print("\n--- DOC", i, "---")
    print("METADATA:", docs["metadatas"][i])
    print("CONTENT:", docs["documents"][i][:120])
