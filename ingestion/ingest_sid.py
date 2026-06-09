from ingestion.extract_pdf import extract_pdf_text
from ingestion.semantic_chunker import semantic_chunk
from ingestion.embedding_service import EmbeddingService
from ingestion.postgres_writer import PostgresWriter


def ingest_sid(
    pdf_path: str,
    scheme_name: str,
    amc_name: str
):

    # Step 1
    pages = extract_pdf_text(pdf_path)

    # Step 2
    chunks = semantic_chunk(pages)

    # Step 3
    embedding_service = EmbeddingService()

    for chunk in chunks:

        chunk["scheme_name"] = scheme_name
        chunk["amc_name"] = amc_name
        chunk["document_type"] = "SID"

        chunk["embedding"] = (
            embedding_service.generate_embedding(
                chunk["chunk_text"]
            )
        )

    # Step 4
    writer = PostgresWriter()

    writer.save_chunks(chunks)

    writer.close()

    print(
        f"Successfully ingested "
        f"{len(chunks)} chunks"
    )