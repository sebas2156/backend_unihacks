from typing import Optional

from sqlalchemy import DateTime, ForeignKeyConstraint, Integer, PrimaryKeyConstraint, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
import datetime
from database import Base

class Logs(Base):
    __tablename__ = 'logs'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['users.id'], name='logs_user_id_fkey'),
        PrimaryKeyConstraint('id', name='logs_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    action_type: Mapped[str] = mapped_column(Text)
    endpoint: Mapped[str] = mapped_column(Text)
    user_id: Mapped[int] = mapped_column(Integer)
    details: Mapped[str] = mapped_column(Text)
    timestamp: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))

    user: Mapped['Users'] = relationship('Users', back_populates='logs')

