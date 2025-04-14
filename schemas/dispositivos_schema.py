from pydantic import BaseModel
from typing import Optional, List
import datetime


class DispositivosCreate(BaseModel):
    codigo_dispositivo: str
    id_usuario: int
    nombre_dispositivo: str
    contraseña: str = None

class DispositivosResponse(DispositivosCreate):
    id: int


class PaginatedDispositivosResponse(BaseModel):
    total_registros: int
    por_pagina: int
    pagina_actual: int
    total_paginas: int
    data: List[DispositivosResponse]
