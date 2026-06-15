# # ingestion/bootstrap/ingestion_container.py

# class IngestionContainer:

#     @staticmethod
#     def build(db):

#         aws = AWS()

#         embedding_generator = (
#             BedrockEmbeddingGenerator(
#                 bedrock_client=aws.bedrock_runtime
#             )
#         )

#         embedding_processor = (
#             EmbeddingProcessor(
#                 ...
#             )
#         )

#         return DocumentIngestionPipeline(
#             pdf_loader=PDFLoader(),
#             metadata_extractor=SchemeMetadataExtractor(),
#             section_parser=SIDParser(),
#             chunker=TokenWindowChunker(),
#             embedding_processor=embedding_processor,
#             document_repository=DocumentRepository(db),
#             document_version_repository=DocumentVersionRepository(db),
#             version_chunk_mapping_repository=VersionChunkMappingRepository(db),
#             db=db,
#         )

from sqlalchemy.orm import Session
from ingestion.pipelines.document_ingestion_pipeline import DocumentIngestionPipeline
from app.core.database import SessionLocal


class IngestionContainer:

    @staticmethod
    def build(db):
        return DocumentIngestionPipeline(db=db)

    # def __init__(self,db: Session) -> None:
    #     self.pipeline= DocumentIngestionPipeline(db=db)