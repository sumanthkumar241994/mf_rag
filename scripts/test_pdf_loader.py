from ingestion.loaders.pdf import PDFLoader
from ingestion.parsers.sid import SIDParser



document = PDFLoader().load("/users/sumanth/downloads/1775025166649.pdf")

print(document.page_count)
print(document.pages[0].content[:1000])


scheme_doc = SIDParser().parse(document=document)