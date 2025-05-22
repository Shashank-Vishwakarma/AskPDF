from fastapi import APIRouter, status, File, UploadFile, Depends, HTTPException
from fastapi.responses import JSONResponse
from typing import Annotated
from src.middlewares import token_bearer
from src.docs_ingestion.service import supabase_service
from src.celery import ingest_docs_into_qdrant

documents_router = APIRouter()

@documents_router.post("/ingest", status_code=status.HTTP_201_CREATED)
async def ingest_documents(
    file: Annotated[UploadFile, File()],
    token_details = Depends(token_bearer)
):
    try:
        pdf_path = supabase_service.upload_file(file=file)

        ingest_docs_into_qdrant.delay(collection_name="pdf_docs", pdf_path=pdf_path)

        return JSONResponse(
            content={
                "message": "Documents ingested successfully",
            },
            status_code=status.HTTP_201_CREATED
        )
    except Exception as e:
        print("ingest_documents API: Error: ", str(e))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))