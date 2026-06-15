from sqlite3 import dbapi2
from sqlalchemy.orm import Session

from app.repositories import ( 
    DocumentChunkRepository, 
    DocumentRepository, 
    VersionChunkMappingRepository, 
    DocumentVersionRepository
)

from ingestion.embeddings.embedding_processor import EmbeddingProcessor
from ingestion.metadata.models.scheme_metadata import SchemeMetaData
from ingestion.chunking.models import Chunk


class DocumentIngestionService:

    def __init__(
        self,
        db: Session,
        document_repository: DocumentRepository,
        chunk_repository: DocumentChunkRepository,
        document_version_repository: DocumentVersionRepository,
        version_chunk_mapping_repository: VersionChunkMappingRepository,
        embedding_processor: EmbeddingProcessor
    ):

        self.db = db
        self.document_repository = document_repository
        self.chunk_repository = chunk_repository
        self.document_version_repository = document_version_repository
        self.version_chunk_mapping_repository = version_chunk_mapping_repository
        self.embedding_processor = embedding_processor

    def ingest(
        self,
        *,
        metadata: SchemeMetaData,
        file_name: str,
        file_hash: str,
        s3_path: str,
        chunks: list[Chunk],
        document_type: str = 'SID',
        scheme_code: str | None = None
    ):
        try:
            # Find the exisiting logical document
            document = self.document_repository.get_by_scheme_and_type(
                scheme_name = metadata.scheme_name,
                document_type=document_type
            )

            # if not exist, create a document
            if not document:
                document = self.document_repository.create(
                    amc_name=metadata.amc_name,
                    scheme_name=metadata.scheme_name,
                    document_type=document_type,
                    scheme_code=scheme_code
                )
            
            # Skip if file is already processed
            existing_version = self.document_version_repository.find_by_hash(file_hash=file_hash)

            if existing_version:
                return existing_version

            # Calculate the next version
            latest_version = self.document_version_repository.get_latest_version(document_id=document.id)
            version_number = latest_version+1 if latest_version else 1

            # Deactivate the previous version
            self.document_version_repository.deactivate_version(document_id=document.id,version_no=latest_version)

            #  create document version
            version = self.document_version_repository.create(
                document_id=document.id,
                version_number=version_number,
                file_name=file_name,
                file_hash=file_hash,
                s3_path=s3_path
            )

            # Process chunks
            for chunk in chunks:
                stored_chunk = self.embedding_processor.process(chunk)

                self.version_chunk_mapping_repository.create(
                    document_version_id=version.id,
                    chunk_id=stored_chunk.id,
                    chunk_order=chunk.metadata.chunk_order,
                    page_number=chunk.metadata.page_number,
                    section_title=chunk.metadata.section_title
                )
            
            self.db.commit()
            return version

        except Exception:
            self.db.rollback()
            raise
        


