from pydantic import BaseModel
from typing import List, Optional

class ReporteCreate(BaseModel):
    nombre: Optional[str] = None
    email: Optional[str] = None
    telefono: Optional[int] = None
    fecha_avistamiento: str
    ubicacion_avistamiento: str
    descripcion: str
    imagen: Optional[str] = None

class ReporteResponse(ReporteCreate):
    id: int

# Nuevo esquema de respuesta para paginación de usuarios
class PaginatedReporteResponse(BaseModel):
    total_registros: int
    por_pagina: int
    pagina_actual: int
    total_paginas: int
    data: List[ReporteResponse]
