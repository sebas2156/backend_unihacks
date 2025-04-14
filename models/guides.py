from sqlalchemy import ForeignKeyConstraint, Integer, PrimaryKeyConstraint, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base

class Guide(Base):
    __tablename__ = 'guide'
    __table_args__ = (
        ForeignKeyConstraint(['author_id'], ['users.id'], name='guide_author_id_fkey'),
        ForeignKeyConstraint(['category_id'], ['guide_categories.id'], name='guide_category_id_fkey'),
        PrimaryKeyConstraint('id', name='guide_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    category_id: Mapped[int] = mapped_column(Integer)
    author_id: Mapped[int] = mapped_column(Integer)
    slug: Mapped[str] = mapped_column(Text)
    title: Mapped[str] = mapped_column(Text)
    subtitle: Mapped[str] = mapped_column(Text)
    content: Mapped[str] = mapped_column(Text)

    author: Mapped['Users'] = relationship('Users', back_populates='guide')
    category: Mapped['GuideCategories'] = relationship('GuideCategories', back_populates='guide')

