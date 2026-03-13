import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pgvector_store import get_postgres_collection

load_dotenv()

PDF_PATH = os.getenv("PDF_PATH")
current_dir = Path(__file__).parent
provider = os.getenv("PROVIDER_LLM")
collection_name = os.getenv("PG_VECTOR_COLLECTION_NAME")
connection_url = os.getenv("DATABASE_URL")
chunk_size = 1000
chunk_overlap = 150


def _validate_required_settings() -> None:
    required_settings = {
        "PDF_PATH": PDF_PATH,
        "PROVIDER_LLM": provider,
        "PG_VECTOR_COLLECTION_NAME": collection_name,
        "DATABASE_URL": connection_url,
    }

    missing_vars = [name for name, value in required_settings.items() if not value]

    if missing_vars:
        raise ValueError(
            "Missing required environment variables: " + ", ".join(missing_vars)
        )

def ingest_pdf():
    _validate_required_settings()
    pdf_path = current_dir / '..' / PDF_PATH
    print(f" Start to Ingesting PDF from path: {pdf_path}")

    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"Arquivo não encontrado: {pdf_path}")

    loader = PyPDFLoader(str(pdf_path)).load()

    splits = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap).split_documents(loader)

    if not splits:
        print("No text found in the PDF.")
        return
    
    enriched_splits = [
        Document(
            page_content=d.page_content,
            metadata={k: v for k, v in d.metadata.items() if v not in ("", None)}
        ) for d in splits
    ]

    ids = [f"doc-{i}" for i in range(len(enriched_splits))]
    store = get_postgres_collection(collection_name=collection_name, connection_url=connection_url)
    store.add_documents(documents=enriched_splits, ids=ids)
    


if __name__ == "__main__":
    ingest_pdf()
