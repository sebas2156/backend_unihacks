from pydantic import BaseModel
from typing import Optional, List
import datetime


class DesaparecidosCreate(BaseModel):
    nombre: str
    apellido: str
    genero: str
    descripcion: str
    fecha_nacimiento: datetime.date
    fecha_desaparicion: datetime.date
    lugar_desaparicion: str
    estado_investigacion: str
    foto_perfil: str
    nombre_reportante: str
    telefono_reportante: str
    foto_suceso: str
    coordenadas: str
    edad: int = None
    caracteristicas: str = None
    id_usuario: int = None

class DesaparecidosResponse(DesaparecidosCreate):
    id: int


class PaginatedDesaparecidosResponse(BaseModel):
    total_registros: int
    por_pagina: int
    pagina_actual: int
    total_paginas: int
    data: List[DesaparecidosResponse]
