from sqlalchemy import Column, Text, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from database import Base

class FAQCategory(Base):
    __tablename__ = 'faq_categories'

    id = Column(Integer, primary_key=True, index=True)
    slug = Column(Text, nullable=False)
    title = Column(Text, nullable=False)

class FAQ(Base):
    __tablename__ = 'fag'

    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, nullable=False)
    author_id = Column(Integer, nullable=False)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)

    #category = relationship('FAQCategory')
