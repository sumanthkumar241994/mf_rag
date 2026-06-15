from ingestion.loaders.pdf import PDFLoader
from ingestion.parsers.sid import SIDParser
from ingestion.metadata.extractor import MetaDataExtractor
from ingestion.chunking.semantic_chunker import SemanticChunker
from ingestion.embeddings.embedding_processor import EmbeddingProcessor

document = PDFLoader().load("/users/sumanth/downloads/1781088432492.pdf")
scheme_doc = SIDParser().parse(document=document)
scheme_metadata = MetaDataExtractor().extract(document=document)
chunks = SemanticChunker().chunk(scheme_doc)

for chunk in chunks:
    EmbeddingProcessor.process(chunk)


    
# print(document.page_count)
# print(document.pages[0].content[:1000])