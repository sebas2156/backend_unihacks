from typing import List

from sqlalchemy import ForeignKeyConstraint, Integer, PrimaryKeyConstraint, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base

class ContactoEmergencia(Base):
    __tablename__ = 'contacto_emergencia'
    __table_args__ = (
        ForeignKeyConstraint(['id_usuario'], ['users.id'], name='contacto_emergencia_id_usuario_fkey'),
        PrimaryKeyConstraint('id', name='contacto_emergencia_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_usuario: Mapped[int] = mapped_column(Integer)
    nombre_contacto: Mapped[str] = mapped_column(Text)
    linea_telefonica: Mapped[str] = mapped_column(Text)
    numero: Mapped[str] = mapped_column(Text)

    users: Mapped['Users'] = relationship('Users', back_populates='contacto_emergencia')
    notificaciones_push: Mapped[List['NotificacionesPush']] = relationship('NotificacionesPush', back_populates='contacto_emergencia')

