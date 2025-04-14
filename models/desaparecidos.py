from typing import List, Optional

from sqlalchemy import ARRAY, Date, ForeignKeyConstraint, Integer, PrimaryKeyConstraint, Sequence, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
import datetime
from database import Base


class Desaparecidos(Base):
    __tablename__ = 'desaparecidos'
    __table_args__ = (
        ForeignKeyConstraint(['id_usuario'], ['users.id'], name='desaparecidos_id_usuario_fkey'),
        PrimaryKeyConstraint('id', name='desaparecidos_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, Sequence('persona_id_seq'), primary_key=True)
    nombre: Mapped[str] = mapped_column(Text)
    apellido: Mapped[str] = mapped_column(Text)
    genero: Mapped[str] = mapped_column(Text)
    descripcion: Mapped[str] = mapped_column(Text)
    fecha_nacimiento: Mapped[datetime.date] = mapped_column(Date)
    fecha_desaparicion: Mapped[datetime.date] = mapped_column(Date)
    lugar_desaparicion: Mapped[str] = mapped_column(Text)
    estado_investigacion: Mapped[str] = mapped_column(Text)
    foto_perfil: Mapped[str] = mapped_column(Text)
    nombre_reportante: Mapped[str] = mapped_column(Text)
    telefono_reportante: Mapped[str] = mapped_column(Text)
    foto_suceso: Mapped[list] = mapped_column(ARRAY(Text()))
    coordenadas: Mapped[list] = mapped_column(ARRAY(Text()))
    edad: Mapped[Optional[int]] = mapped_column(Integer)
    caracteristicas: Mapped[Optional[list]] = mapped_column(ARRAY(Text()))
    id_usuario: Mapped[Optional[int]] = mapped_column(Integer)

    users: Mapped['Users'] = relationship('Users', back_populates='desaparecidos')
    reportes: Mapped[List['Reportes']] = relationship('Reportes', back_populates='desaparecidos')

