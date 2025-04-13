from datetime import datetime

from pydantic import BaseModel
from typing import List, Optional

class SolicitudesCreate(BaseModel):
    codigo_panico: str
    direccion: str
    coordenadas: str
    fecha_hora: datetime
    dispositivo: str

class SolicitudesResponse(SolicitudesCreate):
    id: int

# Nuevo esquema de respuesta para paginación de usuarios
class PaginatedSolicitudesResponse(BaseModel):
    total_registros: int
    por_pagina: int
    pagina_actual: int
    total_paginas: int
    data: List[SolicitudesResponse]
