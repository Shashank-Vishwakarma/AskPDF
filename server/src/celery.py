from celery import Celery

from src.config import Config
from src.docs_ingestion.service import qdrant_service

celery_app = Celery(
    "askpdf",
    broker=Config.REDIS_URL,
    backend=Config.REDIS_URL
)

@celery_app.task
def ingest_docs_into_qdrant(collection_name: str, pdf_path: str):
    qdrant_service.ingest_documents(collection_name=collection_name, pdf_path=pdf_path)
    print("Docs successfully ingested into qdrant!")