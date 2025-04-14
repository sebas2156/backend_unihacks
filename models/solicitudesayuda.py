from typing import List

from sqlalchemy import ARRAY, DateTime, ForeignKeyConstraint, Integer, PrimaryKeyConstraint, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
import datetime
from database import Base

class SolicitudesAyuda(Base):
    __tablename__ = 'solicitudes_ayuda'
    __table_args__ = (
        ForeignKeyConstraint(['codigo_dispositivo'], ['dispositivos.codigo_dispositivo'], name='solicitudes_ayuda_codigo_dispositivo_fkey'),
        PrimaryKeyConstraint('codigo_panico', name='solicitudes_ayuda_pkey')
    )

    codigo_panico: Mapped[int] = mapped_column(Integer, primary_key=True)
    direccion: Mapped[str] = mapped_column(Text)
    coordenadas: Mapped[str] = mapped_column(Text)
    fecha_hora: Mapped[datetime.datetime] = mapped_column(DateTime)
    codigo_dispositivo: Mapped[str] = mapped_column(Text)
    lista_wifi: Mapped[list] = mapped_column(ARRAY(Text()))
    acciones_dispositivo: Mapped[list] = mapped_column(ARRAY(Text()))

    dispositivos: Mapped['Dispositivos'] = relationship('Dispositivos', back_populates='solicitudes_ayuda')
    notificaciones_push: Mapped[List['NotificacionesPush']] = relationship('NotificacionesPush', back_populates='solicitudes_ayuda')

