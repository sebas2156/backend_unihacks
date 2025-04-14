from sqlalchemy import ARRAY, DateTime, ForeignKeyConstraint, Integer, PrimaryKeyConstraint, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
import datetime
from database import Base

class DispositivoRegistro(Base):
    __tablename__ = 'dispositivo_registro'
    __table_args__ = (
        ForeignKeyConstraint(['codigo_dispositivo'], ['dispositivos.codigo_dispositivo'], name='dispositivo_registro_codigo_dispositivo_fkey'),
        PrimaryKeyConstraint('id', 'codigo_dispositivo', name='dispositivo_registro_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    codigo_dispositivo: Mapped[str] = mapped_column(Text, primary_key=True)
    lista_wifi: Mapped[list] = mapped_column(ARRAY(Text()))
    coordenadas: Mapped[list] = mapped_column(ARRAY(Text()))
    fecha_hora_actualizacion: Mapped[datetime.datetime] = mapped_column(DateTime)

    dispositivos: Mapped['Dispositivos'] = relationship('Dispositivos', back_populates='dispositivo_registro')

