from pydantic import BaseModel, deca
from sqlalchemy import Column, String, UUID
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class User(Base):
    _table_name__ = "users"

    id = Column(UUID, primary_key=True)
    email = Column(String, primary_key=True, index=True)
    password = Column(String)
    plan = Column(String)