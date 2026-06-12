from ingestion.loaders.pdf import PDFLoader
from ingestion.parsers.sid import SIDParser



document = PDFLoader().load("/users/sumanth/downloads/1780464572018.pdf")

print(document.page_count)
print(document.pages[0].content[:1000])


scheme_doc = SIDParser().parse(document=document)