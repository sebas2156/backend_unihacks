from pydantic import BaseModel
from typing import List, Optional

class ContactosCreate(BaseModel):
    nombre: str
    telefono: int
    linea_telefonica :int
    accion : str

class ContactosResponse(ContactosCreate):
    id: int

# Esquema de respuesta paginada para personas
class PaginatedContactosResponse(BaseModel):
    total_registros: int
    por_pagina: int
    pagina_actual: int
    total_paginas: int
    data: List[ContactosResponse]
