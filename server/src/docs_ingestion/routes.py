from fastapi import APIRouter, status, File, UploadFile, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import Annotated
from src.middlewares import token_bearer
from src.docs_ingestion.service import supabase_service
from src.celery import ingest_docs_into_qdrant
from src.models import Document
from src.db.main import get_db_session

documents_router = APIRouter()

@documents_router.post("/ingest", status_code=status.HTTP_201_CREATED)
async def ingest_documents(
    file: Annotated[UploadFile, File()],
    token_details = Depends(token_bearer),
    session: AsyncSession = Depends(get_db_session)
):
    try:
        # Upload file to storage
        pdf_path = supabase_service.upload_file(file=file)

        # Ingest pdf into qdrant collection
        ingest_docs_into_qdrant.delay(collection_name="pdf_docs", pdf_path=pdf_path)

        # Create an entry into database
        document = Document(
            pdf_url=pdf_path,
            pdf_name=file.filename,
            user_id=token_details["user"]["id"]
        )

        session.add(document)
        await session.commit()

        return JSONResponse(
            content={
                "message": "Documents ingested successfully",
            },
            status_code=status.HTTP_201_CREATED
        )
    except Exception as e:
        print("ingest_documents API: Error: ", str(e))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))