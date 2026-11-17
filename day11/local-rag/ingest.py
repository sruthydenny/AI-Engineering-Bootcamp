
from pathlib import Path

import chromadb
from openai import OpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pypdf import PdfReader

import config


BASE_DIR = Path(__file__).parent
DOCUMENTS_DIR = BASE_DIR / "documents"
CHROMA_DIR = BASE_DIR / "chroma_db"

# Connect to local Ollama embedding endpoint
embedding_client = OpenAI(
    base_url=config.EMBEDDING_BASE_URL,
    api_key=config.LLM_API_KEY,
)

# Connect to persistent local Chroma database
chroma_client = chromadb.PersistentClient(path=str(CHROMA_DIR))


def get_embeddings(texts: list[str]) -> list[list[float]]:
    response = embedding_client.embeddings.create(
        model=config.EMBEDDING_MODEL,
        input=texts,
    )
    return [item.embedding for item in response.data]


def ingest_documents():
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.CHUNK_SIZE,
        chunk_overlap=config.CHUNK_OVERLAP,
    )

    documents = []
    metadatas = []
    ids = []

    pdf_files = sorted(DOCUMENTS_DIR.glob("*.pdf"))

    if not pdf_files:
        raise FileNotFoundError("No PDF files found in documents/")

    for pdf_path in pdf_files:
        reader = PdfReader(str(pdf_path))
        print(f"Reading: {pdf_path.name}")

        for page_number, page in enumerate(reader.pages, start=1):
            text = page.extract_text(extraction_mode="layout") or ""

            if not text.strip():
                continue

            chunks = splitter.split_text(text)

            for chunk_index, chunk in enumerate(chunks):
                documents.append(chunk)
                metadatas.append({
                    "source": pdf_path.name,
                    "page": page_number,
                    "chunk_index": chunk_index,
                })
                ids.append(
                    f"{pdf_path.stem}-page{page_number}-chunk{chunk_index}"
                )

    if not documents:
        raise ValueError("No text could be extracted from the PDFs.")

    print(f"\nTotal chunks created: {len(documents)}")
    print("\nSample extracted chunk:\n")
    print(documents[0][:500])

    # Rebuild the collection to avoid duplicate chunks on re-ingestion
    try:
        chroma_client.delete_collection(config.COLLECTION_NAME)
    except chromadb.errors.NotFoundError:
        pass

    collection = chroma_client.create_collection(
        name=config.COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )

    # Generate embeddings in batches and store them locally
    batch_size = 32

    for start in range(0, len(documents), batch_size):
        end = start + batch_size
        batch_texts = documents[start:end]

        embeddings = get_embeddings(batch_texts)

        collection.add(
            ids=ids[start:end],
            documents=batch_texts,
            metadatas=metadatas[start:end],
            embeddings=embeddings,
        )

        print(f"Stored {min(end, len(documents))}/{len(documents)} chunks")

    print("\nIngestion complete!")
    print(f"Documents processed: {len(pdf_files)}")
    print(f"Chunks stored: {collection.count()}")
    print(f"Database location: {CHROMA_DIR}")


if __name__ == "__main__":
    ingest_documents()
