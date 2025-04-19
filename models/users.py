from typing import List, Optional

from sqlalchemy import Integer, PrimaryKeyConstraint, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base

class Users(Base):
    __tablename__ = 'users'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='users_pkey'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    codigo_persona: Mapped[str] = mapped_column(Text)
    email: Mapped[str] = mapped_column(Text)
    avatar_imagen: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(Text)
    role: Mapped[str] = mapped_column(Text)
    password: Mapped[str] = mapped_column(Text)
    numero: Mapped[Optional[str]] = mapped_column(Text)
    token_firebase: Mapped[Optional[str]] = mapped_column(Text)
    linea_telefonica: Mapped[Optional[str]] = mapped_column(Text)
    username: Mapped[Optional[str]] = mapped_column(Text)
    name: Mapped[Optional[str]] = mapped_column(Text)

    contacto_emergencia: Mapped[List['ContactoEmergencia']] = relationship('ContactoEmergencia', back_populates='users')
    desaparecidos: Mapped[List['Desaparecidos']] = relationship('Desaparecidos', back_populates='users')
    dispositivos: Mapped[List['Dispositivos']] = relationship('Dispositivos', back_populates='users')
    fag: Mapped[List['Fag']] = relationship('Fag', back_populates='author')
    guide: Mapped[List['Guide']] = relationship('Guide', back_populates='author')
    logs: Mapped[List['Logs']] = relationship('Logs', back_populates='user')
    support_request: Mapped[List['SupportRequest']] = relationship('SupportRequest', back_populates='user')
    reportes: Mapped[List['Reportes']] = relationship('Reportes', back_populates='users')

