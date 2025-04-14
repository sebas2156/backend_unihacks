from sqlalchemy import ForeignKeyConstraint, Integer, PrimaryKeyConstraint, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base

class Fag(Base):
    __tablename__ = 'fag'
    __table_args__ = (
        ForeignKeyConstraint(['author_id'], ['users.id'], name='fag_author_id_fkey'),
        ForeignKeyConstraint(['category_id'], ['faq_categories.id'], name='fag_category_id_fkey'),
        PrimaryKeyConstraint('id', name='fag_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    category_id: Mapped[int] = mapped_column(Integer)
    author_id: Mapped[int] = mapped_column(Integer)
    question: Mapped[str] = mapped_column(Text)
    answer: Mapped[str] = mapped_column(Text)

    author: Mapped['Users'] = relationship('Users', back_populates='fag')
    category: Mapped['FaqCategories'] = relationship('FaqCategories', back_populates='fag')

