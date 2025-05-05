from sqlalchemy import Column, String, UUID
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Document(Base):
    __tablename__ = 'documents'
    
    id = Column(UUID, primary_key=True)
    title = Column(String)
    content = Column(String)
    UserId = Column(UUID)