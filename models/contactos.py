from sqlalchemy import Column, Text, Integer, ARRAY, String
from database import Base

class Contactos(Base):
    __tablename__ = 'contacto_emergencia'

    id = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, nullable=False)
    nombre_contacto = Column(Text, nullable=False)
    linea_telefonica = Column(Text, nullable=False)
    numero = Column(Integer, nullable=False)
