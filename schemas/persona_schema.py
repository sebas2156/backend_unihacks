from pydantic import BaseModel
from typing import List, Optional

class PersonaCreate(BaseModel):
    nombre: str
    apellido: str
    edad: Optional[int] = None
    genero: str
    descripcion: str
    fecha_nacimiento: str
    fecha_desaparicion: str
    lugar_desaparicion: str
    estado_investigacion: str
    foto: str
    caracteristicas: Optional[List[str]] = None

class PersonaResponse(PersonaCreate):
    id: int

# Esquema de respuesta paginada para personas
class PaginatedPersonaResponse(BaseModel):
    total_registros: int
    por_pagina: int
    pagina_actual: int
    total_paginas: int
    data: List[PersonaResponse]
