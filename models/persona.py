from sqlalchemy import Column, Text, Integer, ARRAY, String
from sqlalchemy.dialects.postgresql import UUID
from database import Base

class Persona(Base):
    __tablename__ = 'persona'

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(Text, nullable=False)
    apellido = Column(Text, nullable=False)
    edad = Column(Integer, nullable=True)
    genero = Column(Text, nullable=False)
    descripcion = Column(Text, nullable=False)
    fecha_nacimiento = Column(Text, nullable=False)
    fecha_desaparicion = Column(Text, nullable=False)
    lugar_desaparicion = Column(Text, nullable=False)
    estado_investigacion = Column(Text, nullable=False)
    fecha_desaparicion = Column(Text, nullable=False)
    foto = Column(Text, nullable=False)
    caracteristicas = Column(ARRAY(String), nullable=True)
