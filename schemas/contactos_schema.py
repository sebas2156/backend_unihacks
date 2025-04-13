from pydantic import BaseModel
from typing import List, Optional

class ContactosCreate(BaseModel):
    id_usuario: int
    nombre_contacto: str
    linea_telefonica: str
    numero: int

class ContactosResponse(ContactosCreate):
    id: int

# Esquema de respuesta paginada para personas
class PaginatedContactosResponse(BaseModel):
    total_registros: int
    por_pagina: int
    pagina_actual: int
    total_paginas: int
    data: List[ContactosResponse]
