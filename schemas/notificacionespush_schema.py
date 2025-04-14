from pydantic import BaseModel
from typing import Optional, List
import datetime


class NotificacionesPushCreate(BaseModel):
    codigo_panico: int
    titulo: str
    contenido: str
    id_contacto: int

class NotificacionesPushResponse(NotificacionesPushCreate):
    id: int


class PaginatedNotificacionesPushResponse(BaseModel):
    total_registros: int
    por_pagina: int
    pagina_actual: int
    total_paginas: int
    data: List[NotificacionesPushResponse]
