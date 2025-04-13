from sqlalchemy import Column, Integer, String
from database import Base

class Dispositivos(Base):
    __tablename__ = 'dispositivos'

    codigo_dispositivo = Column(String, primary_key=True, index=True)
    id_usuario = Column(Integer, nullable=False)
    nombre_contacto = Column(String, nullable=False)
