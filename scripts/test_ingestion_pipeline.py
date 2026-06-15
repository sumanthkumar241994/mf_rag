from nt import pipe
from ingestion.bootstrap.ingestion_container import IngestionContainer
from app.core.database import SessionLocal

db = SessionLocal()
try:
    pipeline = IngestionContainer.build(db)
    # pipeline = container.pipeline
    pipeline.run(file_path="/Users/sumanth/Downloads/1781088432492.pdf", s3_path="local-test")
finally:
    db.close()

