from typing import List

from sqlalchemy import Integer, PrimaryKeyConstraint, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base

class GuideCategories(Base):
    __tablename__ = 'guide_categories'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='guide_categories_pkey'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    slug: Mapped[str] = mapped_column(Text)
    title: Mapped[str] = mapped_column(Text)

    guide: Mapped[List['Guide']] = relationship('Guide', back_populates='category')

