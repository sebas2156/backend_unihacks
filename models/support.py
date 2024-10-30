from sqlalchemy import Column, Text, ForeignKey, TIMESTAMP, Integer
from sqlalchemy.dialects.postgresql import UUID
from database import Base

class SupportRequest(Base):
    __tablename__ = 'support_request'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    name = Column(Text, nullable=False)
    email = Column(Text, nullable=False)
    subject = Column(Text, nullable=False)
    message = Column(Text, nullable=False)
    sent_at = Column(TIMESTAMP, nullable=False)
