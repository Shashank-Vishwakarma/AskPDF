from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, UUID

Base = declarative_base()

class Message(Base):
    __tablename__ = 'messages'

    id = Column(UUID, primary_key=True)
    message = Column(String)
    role = Column(String)
    UserId = Column(UUID)