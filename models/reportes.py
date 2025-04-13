from sqlalchemy import Column, Text, Integer
from sqlalchemy.dialects.postgresql import UUID
from database import Base

class Reporte(Base):
    __tablename__ = 'reportes'

    id = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, nullable=False)
    id_persona = Column(Integer, nullable=False)
    nombre = Column(Text, nullable=True)
    email = Column(Text, nullable=True)
    telefono = Column(Integer, nullable=True)
    fecha_avistamiento = Column(Text, nullable=False)
    ubicacion_avistamiento = Column(Text, nullable=False)
    descripcion = Column(Text, nullable=False)
    imagen = Column(Text, nullable=True)
