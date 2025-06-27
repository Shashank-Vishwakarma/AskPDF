from fastapi import APIRouter, status, File, UploadFile, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import update, select
from typing import Annotated
from src.middlewares import token_bearer
from src.docs_ingestion.service import supabase_service, qdrant_service, ai_service
from src.celery import ingest_docs_into_qdrant
from src.models import Document
from src.db.main import get_db_session
from src.docs_ingestion.schemas import UpdateInsertStatus, ChatRequestBody
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
        ingest_docs_into_qdrant.delay(collection_name="pdf_docs", pdf_path=pdf_path, token=token_details["token"], user_id=token_details["user"]["id"])

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
        statement = select(Document).where(models.Document.pdf_url == body.pdf_path).where(Document.user_id == token_details["user"]["id"])
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
            "url": data.pdf_url, 
            "insert_status": data.insert_status
        }

        return JSONResponse(content=doc, status_code=status.HTTP_200_OK)
    except Exception as e:
        print(f"get_pdf_details: Error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@documents_router.get("/{doc_id}/user/pdf/chats")
async def get_chats(
    doc_id: str,
    token_details = Depends(token_bearer),
    session: AsyncSession = Depends(get_db_session)
):
    try:
        statement = select(Document).where(Document.id == doc_id).where(Document.user_id == token_details["user"]["id"])
        result = await session.exec(statement)
        data = result.first()
        if not data:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")

        statement = select(models.Chat).where(models.Chat.user_id == token_details["user"]["id"]).where(models.Chat.pdf_id == doc_id)
        result = await session.exec(statement)
        chats = result.all()

        conversations = [{"id": chat.id.hex, "role": chat.role, "content": chat.content, "created_at": chat.created_at.strftime("%Y-%m-%d %H:%M:%S")} for chat in chats]
        return JSONResponse(content=conversations, status_code=status.HTTP_200_OK)
    except Exception as e:
        print(f"get_chats: Error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@documents_router.post("/{doc_id}/chats")
async def chat(
    doc_id: str,
    body: ChatRequestBody,
    token_details = Depends(token_bearer),
    session: AsyncSession = Depends(get_db_session)
):
    try:
        request_body = body.dict()

        # Check user has the pdf
        statement = select(Document).where(Document.id == doc_id).where(Document.user_id == token_details["user"]["id"])
        result = await session.exec(statement)
        data = result.first()
        if not data:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")

        # Save user query
        chat = models.Chat(user_id=token_details["user"]["id"], pdf_id=doc_id, role="user", content=request_body["query"])
        session.add(chat)
        await session.commit()

        # Get the previous conversations
        statement = select(models.Chat).where(models.Chat.user_id == token_details["user"]["id"]).where(models.Chat.pdf_id == doc_id).order_by(models.Chat.created_at)
        result = await session.exec(statement)
        conversations = result.all()
        chat_history = [{"role": chat.role, "content": chat.content} for chat in conversations]

        # Retrieve data from qdrant
        context_documents = qdrant_service.retrieve_documents(collection_name="pdf_docs", query=request_body["query"], user_id=token_details["user"]["id"], pdf_url=data.pdf_url, limit=5)

        messages = [
            {
                "role": "system",
                "content": """
                    You are a helpful AI assistant.
                    You are given the following extracted parts of a long document and a question.
                    Provide a conversational answer.
                    Construct a response that appropriately completes the question.

                    Constraints:
                    1. Avoid repeating information.
                    2. Answer the question as concisely as possible.
                    
                    Return answer as string output in markdown format.
                """
            },
        ]
        messages.extend(chat_history)
        messages.extend([{"role": "user", "content": doc} for doc in context_documents])
        messages.append({"role": "user", "content": request_body["query"]})

        # Get response from AI
        response = ai_service.get_ai_response(messages)

        # Save user query
        chat = models.Chat(user_id=token_details["user"]["id"], pdf_id=doc_id, role="assistant", content=response)
        session.add(chat)
        await session.commit()

        return JSONResponse(content={"response": response}, status_code=status.HTTP_200_OK)
    except Exception as e:
        print(f"chat: Error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))