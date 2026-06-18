from pathlib import Path
import hashlib
import tempfile

from sqlalchemy.orm import Session

from app.repositories import DocumentRepository, DocumentVersionRepository, VersionChunkMappingRepository
from app.core.config.aws import AWS
from ingestion.loaders.pdf import PDFLoader
from ingestion.parsers.sid import SIDParser
from ingestion.metadata.extractor import MetaDataExtractor
from ingestion.chunking.semantic_chunker import SemanticChunker
from ingestion.embeddings.embedding_processor import EmbeddingProcessor


class DocumentIngestionPipeline:
    def __init__(
        self,
        db: Session
    ):
        self.pdf_loader = PDFLoader()
        self.metadata_extractor = MetaDataExtractor()
        self.sid_parser = SIDParser()
        self.chunker = SemanticChunker()
        self.embedding_processor = EmbeddingProcessor(db)
        self.document_repository = DocumentRepository(db)
        self.document_version_repository = DocumentVersionRepository(db)
        self.version_chunk_mapping_repository = VersionChunkMappingRepository(db)
        self.aws = AWS()
        self.db = db

    def run(self, *, file_path: str, s3_path: str, document_type: str = 'SID', scheme_code: str | None = None):
        try:
            # Load PDF
            parsed_document =  self.pdf_loader.load(file_path=file_path)
            # Extract Metadata
            metadata = self.metadata_extractor.extract(document=parsed_document)
            #Generate File hash
            file_hash = self._generate_file_hash(file_path)

            # Find/create logical document
            document = self.document_repository.get_by_scheme_and_type(
                scheme_name=metadata.scheme_name,
                document_type=document_type
                )
            
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
                return {
                    "status": "Skipped",
                    "reason": "Duplicate file",
                    "document_id": document.id,
                    "version_id": existing_version.id
                }
            
            # Parse sections
            scheme_doc = self.sid_parser.parse(document=parsed_document)

            # Create chunks
            chunks = self.chunker.chunk(scheme_doc=scheme_doc)

            # Determine the latest version
            latest_version = self.document_version_repository.get_latest_version(document_id=document.id)
            version_number = latest_version+1 if latest_version else 1

            # deactivate old versions
            self.document_version_repository.deactivate_version(document_id=document.id, version_no=latest_version)

            # create document version
            version = self.document_version_repository.create(
                document_id=document.id,
                version_number=version_number,
                file_name=Path(file_path).name,
                file_hash=file_hash,
                s3_path=s3_path
            )

            # process chunks
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

            return {
                "status": "Success",
                "document_id": document.id,
                "version_id": version.id,
                "chunk_count": len(chunks)
            }


        except Exception:
            self.db.rollback()
            raise
    
    def run_from_s3(self,*,bucket: str, key: str, document_type: str='SID', scheme_code: str | None = None):
        s3 = self.aws.s3
        suffix=Path(key).suffix or 'pdf'
        with tempfile.NamedTemporaryFile(
            suffix=suffix,
            delete=False,
        ) as temp_file:
            local_file_path = temp_file.name

            try:
                s3.download_file(bucket, key, local_file_path)
                return self.run(
                    file_path=local_file_path,
                    s3_path=f"s3://{bucket}/{key}"
                    ) 

            finally:
                Path(local_file_path).unlink(missing_ok=True)


    def _generate_file_hash(self, file_path: str) -> str:
        with open(file_path, "rb") as file:
            return hashlib.sha256(file.read()).hexdigest()