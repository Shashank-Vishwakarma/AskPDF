from celery import Celery
import requests
import json

from src.config import Config
from src.docs_ingestion.service import qdrant_service

celery_app = Celery(
    "askpdf",
    broker=Config.REDIS_URL,
    backend=Config.REDIS_URL
)

@celery_app.task
def ingest_docs_into_qdrant(collection_name: str, pdf_path: str, token: str):
    try:
        qdrant_service.ingest_documents(collection_name=collection_name, pdf_path=pdf_path)

        response = requests.patch(
            "http://localhost:8000/api/v1/documents/update/status",
            data=json.dumps({
                "pdf_path": pdf_path,
                "insert_status": True
            }),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )

        if response.status_code != 200:
            raise Exception("ingest_docs_into_qdrant: Error making a patch request to update status")

        print("ingest_docs_into_qdrant: Document ingested successfully")
    except Exception as e:
        print("ingest_docs_into_qdrant: Error: ", str(e))
        raise Exception("ingest_docs_into_qdrant: Error ingesting the document")