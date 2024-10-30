from sqlalchemy import Column, Text, Integer
from sqlalchemy.dialects.postgresql import UUID
from database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, nullable=False)
    password = Column(Text, nullable=False)
    email = Column(Text, nullable=False)
    avatar = Column(Text, nullable=False)
    status = Column(Text, nullable=False)
    role = Column(Text, nullable=False)
