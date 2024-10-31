from pydantic import BaseModel
from uuid import UUID
from typing import List

class GuideCategoryCreate(BaseModel):
    slug: str
    title: str

class GuideCategoryResponse(GuideCategoryCreate):
    id: int

class GuideCreate(BaseModel):
    category_id: int
    author_id: int
    slug: str
    title: str
    subtitle: str
    content: str

class GuideResponse(GuideCreate):
    id: UUID

class PaginatedResponse(BaseModel):
    total_registros: int
    por_pagina: int
    pagina_actual: int
    total_paginas: int
    data: List[GuideCategoryResponse]