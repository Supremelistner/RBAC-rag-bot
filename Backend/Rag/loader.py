import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


def normalize_role(folder: str):
    """Convert folder name to a clean role."""
    f = folder.lower()

    if "marketing" in f:
        return "Marketing"
    if "finance" in f:
        return "Finance"
    if "employee" in f:
        return "Employee"
    if "management" in f:
        return "Management"

    return "General"


def load_documents(base_dir: str):
    """
    Loads PDF documents from department folders.
    Automatically assigns role & source metadata.
    """

    all_docs = []
    print(f"[INGEST] Scanning folder: {base_dir}")

    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.lower().endswith(".pdf"):
                full_path = os.path.join(root, file)

                folder_name = os.path.basename(root)
                role = normalize_role(folder_name)

                print(f"[INGEST] Loading PDF: {file} (role={role})")

                loader = PyPDFLoader(full_path)
                pages = loader.load()

                for doc in pages:
                    doc.metadata["role"] = role
                    doc.metadata["source"] = full_path
                    all_docs.append(doc)

    print(f"[INGEST] Loaded {len(all_docs)} raw pages")

    # Split documents into chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
        length_function=len
    )

    final_docs = splitter.split_documents(all_docs)
    print(f"[INGEST] Split into {len(final_docs)} chunks")

    return final_docs
