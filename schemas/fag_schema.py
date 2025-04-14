from pydantic import BaseModel
from typing import Optional, List
import datetime


class FagCreate(BaseModel):
    category_id: int
    author_id: int
    question: str
    answer: str

class FagResponse(FagCreate):
    id: int


class PaginatedFagResponse(BaseModel):
    total_registros: int
    por_pagina: int
    pagina_actual: int
    total_paginas: int
    data: List[FagResponse]
