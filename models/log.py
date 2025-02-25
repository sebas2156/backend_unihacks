from sqlalchemy import Column, Integer, Text, DateTime
from sqlalchemy.sql import func
from database import Base

class Log(Base):
    __tablename__ = 'logs'

    id = Column(Integer, primary_key=True, index=True)
    action_type = Column(Text, nullable=False)  # POST, PUT, DELETE
    endpoint = Column(Text, nullable=False)
    user_id = Column(Integer, nullable=False)  # Asumiendo que el usuario tiene un ID numérico
    timestamp = Column(DateTime, default=func.now())
    details = Column(Text, nullable=True)  # Detalles de la operación si es necesario
