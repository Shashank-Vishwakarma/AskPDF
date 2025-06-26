from pydantic import BaseModel

class UpdateInsertStatus(BaseModel):
    insert_status: bool
    pdf_path: str

class ChatRequestBody(BaseModel):
    query: str