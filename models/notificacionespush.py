from sqlalchemy import ForeignKeyConstraint, Integer, PrimaryKeyConstraint, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base

class NotificacionesPush(Base):
    __tablename__ = 'notificaciones_push'
    __table_args__ = (
        ForeignKeyConstraint(['codigo_panico'], ['solicitudes_ayuda.codigo_panico'], name='notificaciones_push_codigo_panico_fkey'),
        ForeignKeyConstraint(['id_contacto'], ['contacto_emergencia.id'], name='fk_notificaciones_push_id_contacto'),
        PrimaryKeyConstraint('id', name='notificaciones_push_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    codigo_panico: Mapped[int] = mapped_column(Integer)
    titulo: Mapped[str] = mapped_column(Text)
    contenido: Mapped[str] = mapped_column(Text)
    id_contacto: Mapped[int] = mapped_column(Integer)

    solicitudes_ayuda: Mapped['SolicitudesAyuda'] = relationship('SolicitudesAyuda', back_populates='notificaciones_push')
    contacto_emergencia: Mapped['ContactoEmergencia'] = relationship('ContactoEmergencia', back_populates='notificaciones_push')
