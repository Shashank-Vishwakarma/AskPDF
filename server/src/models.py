from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg
import uuid
from datetime import datetime
from typing import Optional

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID(as_uuid=True),
            primary_key=True,
            unique=True,
            nullable=False,
            default=uuid.uuid4,
        )
    )

    name: str = Field(sa_column=Column(pg.TEXT, nullable=False))
    email: str = Field(sa_column=Column(pg.TEXT, unique=True, nullable=False))
    password: str = Field(sa_column=Column(pg.TEXT, nullable=False))
    plan: str = Field(sa_column=Column(pg.TEXT, nullable=False))

    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now(), nullable=False))
    
    def __repr__(self) -> str:
        return f"<User {self.email}>"

class Document(SQLModel, table=True):
    __tablename__ = "documents"

    id: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID(as_uuid=True),
            primary_key=True,
            unique=True,
            nullable=False,
            default=uuid.uuid4,
        )
    )

    pdf_url: str
    pdf_name: str
    insert_status: bool = False

    user_id: Optional[uuid.UUID]  = Field(default=None, foreign_key="users.id")

    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now(), nullable=False))

    def __repr__(self) -> str:
        return f"<Document {self.pdf_name}>"

class Chat(SQLModel, table=True):
    __tablename__ = "chats"

    id: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID(as_uuid=True),
            primary_key=True,
            unique=True,
            nullable=False,
            default=uuid.uuid4,
        )
    )

    user_id: Optional[uuid.UUID]  = Field(default=None, foreign_key="users.id")
    pdf_id: Optional[uuid.UUID] = Field(default=None, foreign_key="documents.id")
    role: str = Field(sa_column=Column(pg.ENUM("user", "assistant", name="role"), nullable=False))
    content: str

    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now(), nullable=False))