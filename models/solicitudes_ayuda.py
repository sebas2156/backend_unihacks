from sqlalchemy import Column, Text, String, DateTime
from sqlalchemy.sql import func
from database import Base

class Solicitudes(Base):
    __tablename__ = 'solicitudes_ayuda'

    codigo_panico = Column(String, primary_key=True, index=True)
    direccion = Column(Text, nullable=False)
    coordenadas = Column(Text, nullable=False)
    fecha_hora = Column(DateTime, default=func.now())
    dispositivo = Column(String, nullable=True)
