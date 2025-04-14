from pydantic import BaseModel
from typing import Optional, List
import datetime


class ReportesCreate(BaseModel):
    fecha_avistamiento: datetime.datetime
    ubicacion_avistamiento: str
    descripcion: str
    id_usuario: int = None
    id_desaparecido: int = None
    nombre_reportante: str = None
    email: str = None
    telefono: str = None
    imagen: str = None
    coordenadas: str = None

class ReportesResponse(ReportesCreate):
    id: int


class PaginatedReportesResponse(BaseModel):
    total_registros: int
    por_pagina: int
    pagina_actual: int
    total_paginas: int
    data: List[ReportesResponse]
