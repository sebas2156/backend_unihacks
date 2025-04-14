from sqlalchemy import DateTime, ForeignKeyConstraint, Integer, PrimaryKeyConstraint, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
import datetime
from database import Base

class SupportRequest(Base):
    __tablename__ = 'support_request'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['users.id'], name='support_request_user_id_fkey'),
        PrimaryKeyConstraint('id', name='support_request_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer)
    name: Mapped[str] = mapped_column(Text)
    email: Mapped[str] = mapped_column(Text)
    subject: Mapped[str] = mapped_column(Text)
    message: Mapped[str] = mapped_column(Text)
    sent_at: Mapped[datetime.datetime] = mapped_column(DateTime)

    user: Mapped['Users'] = relationship('Users', back_populates='support_request')

