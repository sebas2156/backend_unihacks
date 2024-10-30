from sqlalchemy import Column, Text, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from database import Base

class GuideCategory(Base):
    __tablename__ = 'guide_categories'

    id = Column(Integer, primary_key=True, index=True)
    slug = Column(Text, nullable=False)
    title = Column(Text, nullable=False)

class Guide(Base):
    __tablename__ = 'guides'

    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, nullable=False)
    author_id = Column(Integer, nullable=False)
    slug = Column(Text, nullable=False)
    title = Column(Text, nullable=False)
    subtitle = Column(Text, nullable=False)
    content = Column(Text, nullable=False)

    #category = relationship('GuideCategory')
