from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg
import uuid
from datetime import datetime

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            primary_key=True,
            unique=True,
            nullable=False,
        )
    )

    name: str = Field(sa_column=Column(pg.TEXT, nullable=False))
    email: str = Field(sa_column=Column(pg.TEXT, unique=True, nullable=False))
    password: str = Field(sa_column=Column(pg.TEXT, nullable=False))

    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now(), nullable=False))
    
    def __repr__(self) -> str:
        return f"<User {self.email}>"