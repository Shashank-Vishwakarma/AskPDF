from fastapi import APIRouter, status, File, UploadFile, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import update, select
from typing import Annotated
from src.middlewares import token_bearer
from src.docs_ingestion.service import supabase_service
from src.celery import ingest_docs_into_qdrant
from src.models import Document
from src.db.main import get_db_session
from src.docs_ingestion.schemas import UpdateInsertStatus
from src import models

documents_router = APIRouter()

@documents_router.post("/ingest", status_code=status.HTTP_201_CREATED)
async def ingest_documents(
    file: Annotated[UploadFile, File()],
    token_details = Depends(token_bearer),
    session: AsyncSession = Depends(get_db_session),
):
    try:
        # Upload file to storage
        pdf_path = supabase_service.upload_file(file=file)

        # Create an entry into database
        document = Document(
            pdf_url=pdf_path,
            pdf_name=file.filename,
            user_id=token_details["user"]["id"],
            insert_status=False
        )

        session.add(document)
        await session.commit()

        # Ingest pdf into qdrant collection
        ingest_docs_into_qdrant.delay(collection_name="pdf_docs", pdf_path=pdf_path, token=token_details["token"])

        return JSONResponse(
            content={
                "message": "Documents ingested successfully",
            },
            status_code=status.HTTP_201_CREATED
        )
    except Exception as e:
        print("ingest_documents API: Error: ", str(e))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@documents_router.patch("/update/status")
async def update_docs_ingestion_status(
    body: UpdateInsertStatus,
    token_details = Depends(token_bearer),
    session: AsyncSession = Depends(get_db_session)
):
    try:
        statement = select(Document).where(models.Document.pdf_url == body.pdf_path)
        result = await session.exec(statement)
        if result.first() is None:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Document not found")

        statement = update(Document).where(models.Document.pdf_url == body.pdf_path).values(
            insert_status=body.insert_status
        )
        await session.exec(statement)
        await session.commit()

        return JSONResponse(content={"message": "Status updated successfully"}, status_code=status.HTTP_200_OK)
    except Exception as e:
        print(f"get_docs_ingestion_status: Error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@documents_router.get("/all")
async def get_all_docs(
    token_details = Depends(token_bearer),
    session: AsyncSession = Depends(get_db_session)
):
    try:
        statement = select(Document).where(Document.user_id == token_details["user"]["id"])
        result = await session.exec(statement)

        docs = [{"id": doc.id.hex, "pdf_name": doc.pdf_name, "created_at": doc.created_at.strftime("%Y-%m-%d")} for doc in result.all()]
        return JSONResponse(content={"documents": docs}, status_code=status.HTTP_200_OK)
    except Exception as e:
        print(f"get_docs_ingestion_status: Error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@documents_router.delete("/{doc_id}")
async def delete_pdf(
    doc_id: str,
    token_details = Depends(token_bearer),
    session: AsyncSession = Depends(get_db_session)
):
    try:
        statement = select(Document).where(Document.id == doc_id).where(Document.user_id == token_details["user"]["id"])
        result = await session.exec(statement)
        
        data = result.first()
        if data is None:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")

        pdf_path = data.pdf_url.split("/")[-1]
        supabase_service.delete_file(pdf_path)
        await session.delete(data)
        await session.commit()

        return JSONResponse(content={"message": "Document deleted successfully"}, status_code=status.HTTP_200_OK)
    except Exception as e:
        print(f"delete_pdf: Error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@documents_router.get("/{doc_id}")
async def get_pdf_details(
    doc_id: str,
    token_details = Depends(token_bearer),
    session: AsyncSession = Depends(get_db_session)
):
    try:
        statement = select(Document).where(Document.id == doc_id).where(Document.user_id == token_details["user"]["id"])
        result = await session.exec(statement)

        data = result.first()
        if data is None:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")

        doc = {
            "id": data.id.hex,
            "name": data.pdf_name,
            "url": data.pdf_url
        }

        return JSONResponse(content=doc, status_code=status.HTTP_200_OK)
    except Exception as e:
        print(f"get_pdf_details: Error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))