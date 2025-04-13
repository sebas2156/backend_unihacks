from pydantic import BaseModel
from typing import List

class DispositivoCreate(BaseModel):
    codigo_dispositivo: str
    id_usuario: str
    nombre_contacto: str

class DispositivoResponse(DispositivoCreate):
    codigo_dispositivo: str

# Nuevo esquema de respuesta para paginación de usuarios
class PaginatedDispositivoResponse(BaseModel):
    total_registros: int
    por_pagina: int
    pagina_actual: int
    total_paginas: int
    data: List[DispositivoResponse]
