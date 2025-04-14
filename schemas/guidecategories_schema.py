from pydantic import BaseModel
from typing import Optional, List
import datetime


class GuideCategoriesCreate(BaseModel):
    slug: str
    title: str

class GuideCategoriesResponse(GuideCategoriesCreate):
    id: int


class PaginatedGuideCategoriesResponse(BaseModel):
    total_registros: int
    por_pagina: int
    pagina_actual: int
    total_paginas: int
    data: List[GuideCategoriesResponse]
