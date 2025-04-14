from pydantic import BaseModel
from typing import Optional, List
import datetime


class FaqCategoriesCreate(BaseModel):
    slug: str
    title: str

class FaqCategoriesResponse(FaqCategoriesCreate):
    id: int


class PaginatedFaqCategoriesResponse(BaseModel):
    total_registros: int
    por_pagina: int
    pagina_actual: int
    total_paginas: int
    data: List[FaqCategoriesResponse]
