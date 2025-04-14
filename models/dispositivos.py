from typing import List, Optional

from sqlalchemy import ForeignKeyConstraint, Integer, PrimaryKeyConstraint, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base

class Dispositivos(Base):
    __tablename__ = 'dispositivos'
    __table_args__ = (
        ForeignKeyConstraint(['id_usuario'], ['users.id'], name='dispositivos_id_usuario_fkey'),
        PrimaryKeyConstraint('codigo_dispositivo', name='dispositivos_pkey')
    )

    codigo_dispositivo: Mapped[str] = mapped_column(Text, primary_key=True)
    id_usuario: Mapped[int] = mapped_column(Integer)
    nombre_dispositivo: Mapped[str] = mapped_column(Text)
    contraseña: Mapped[Optional[str]] = mapped_column(Text)

    users: Mapped['Users'] = relationship('Users', back_populates='dispositivos')
    dispositivo_registro: Mapped[List['DispositivoRegistro']] = relationship('DispositivoRegistro', back_populates='dispositivos')
    solicitudes_ayuda: Mapped[List['SolicitudesAyuda']] = relationship('SolicitudesAyuda', back_populates='dispositivos')

