from ingestion.loaders.pdf import PDFLoader
from ingestion.parsers.sid import SIDParser
from ingestion.metadata.extractor import MetaDataExtractor

document = PDFLoader().load("/users/sumanth/downloads/1780464572018.pdf")
scheme_doc = SIDParser().parse(document=document)
scheme_metadata = MetaDataExtractor().extract(document=document)
# print(document.page_count)
# print(document.pages[0].content[:1000])