from typing import Optional

from sqlalchemy import ARRAY, DateTime, ForeignKeyConstraint, Integer, PrimaryKeyConstraint, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
import datetime
from database import Base

class Reportes(Base):
    __tablename__ = 'reportes'
    __table_args__ = (
        ForeignKeyConstraint(['id_desaparecido'], ['desaparecidos.id'], name='reportes_id_desaparecido_fkey'),
        ForeignKeyConstraint(['id_usuario'], ['users.id'], name='reportes_id_usuario_fkey'),
        PrimaryKeyConstraint('id', name='reportes_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    fecha_avistamiento: Mapped[datetime.datetime] = mapped_column(DateTime)
    ubicacion_avistamiento: Mapped[str] = mapped_column(Text)
    descripcion: Mapped[str] = mapped_column(Text)
    id_usuario: Mapped[Optional[int]] = mapped_column(Integer)
    id_desaparecido: Mapped[Optional[int]] = mapped_column(Integer)
    nombre_reportante: Mapped[Optional[str]] = mapped_column(Text)
    email: Mapped[Optional[str]] = mapped_column(Text)
    telefono: Mapped[Optional[str]] = mapped_column(Text)
    imagen: Mapped[Optional[list]] = mapped_column(ARRAY(Text()))
    coordenadas: Mapped[Optional[list]] = mapped_column(ARRAY(Text()))

    desaparecidos: Mapped['Desaparecidos'] = relationship('Desaparecidos', back_populates='reportes')
    users: Mapped['Users'] = relationship('Users', back_populates='reportes')

