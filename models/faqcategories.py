from typing import List

from sqlalchemy import Integer, PrimaryKeyConstraint, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base

class FaqCategories(Base):
    __tablename__ = 'faq_categories'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='faq_categories_pkey'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    slug: Mapped[str] = mapped_column(Text)
    title: Mapped[str] = mapped_column(Text)

    fag: Mapped[List['Fag']] = relationship('Fag', back_populates='category')

