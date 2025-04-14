from pydantic import BaseModel
from typing import Optional, List
import datetime


class ContactoEmergenciaCreate(BaseModel):
    id_usuario: int
    nombre_contacto: str
    linea_telefonica: str
    numero: str

class ContactoEmergenciaResponse(ContactoEmergenciaCreate):
    id: int


class PaginatedContactoEmergenciaResponse(BaseModel):
    total_registros: int
    por_pagina: int
    pagina_actual: int
    total_paginas: int
    data: List[ContactoEmergenciaResponse]
