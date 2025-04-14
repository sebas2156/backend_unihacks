from pydantic import BaseModel
from typing import Optional, List
import datetime


class DispositivoRegistroCreate(BaseModel):
    codigo_dispositivo: str
    lista_wifi: str
    coordenadas: str
    fecha_hora_actualizacion: datetime.datetime

class DispositivoRegistroResponse(DispositivoRegistroCreate):
    id: int


class PaginatedDispositivoRegistroResponse(BaseModel):
    total_registros: int
    por_pagina: int
    pagina_actual: int
    total_paginas: int
    data: List[DispositivoRegistroResponse]
