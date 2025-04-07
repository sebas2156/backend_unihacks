from sqlalchemy import Column, Text, Integer, ARRAY, String
from sqlalchemy.dialects.postgresql import UUID
from database import Base

class Contactos(Base):
    __tablename__ = 'contactos'

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(Text, nullable=False)
    telefono = Column(Integer, nullable=False)
    linea_telefonica = Column(Text, nullable=False)
    accion = Column(Text, nullable=False)
