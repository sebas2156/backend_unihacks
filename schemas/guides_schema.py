from pydantic import BaseModel
from typing import Optional, List
import datetime


class GuidesCreate(BaseModel):
    category_id: int
    author_id: int
    slug: str
    title: str
    subtitle: str
    content: str

class GuidesResponse(GuidesCreate):
    id: int


class PaginatedGuidesResponse(BaseModel):
    total_registros: int
    por_pagina: int
    pagina_actual: int
    total_paginas: int
    data: List[GuidesResponse]
