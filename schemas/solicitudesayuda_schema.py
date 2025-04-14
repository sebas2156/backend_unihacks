from pydantic import BaseModel
from typing import Optional, List
import datetime


class SolicitudesAyudaCreate(BaseModel):
    codigo_panico: int
    direccion: str
    coordenadas: str
    fecha_hora: datetime.datetime
    codigo_dispositivo: str
    lista_wifi: str
    acciones_dispositivo: str

class SolicitudesAyudaResponse(SolicitudesAyudaCreate):
    id: int


class PaginatedSolicitudesAyudaResponse(BaseModel):
    total_registros: int
    por_pagina: int
    pagina_actual: int
    total_paginas: int
    data: List[SolicitudesAyudaResponse]
