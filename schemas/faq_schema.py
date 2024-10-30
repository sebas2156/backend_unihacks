from pydantic import BaseModel
from uuid import UUID
from typing import List

class FAQCategoryCreate(BaseModel):
    slug: str
    title: str

class FAQCategoryResponse(FAQCategoryCreate):
    id: int

class FAQCreate(BaseModel):
    category_id: int
    author_id: int
    question: str
    answer: str

class FAQResponse(FAQCreate):
    id: int

# Nuevo esquema de respuesta para paginación
class PaginatedResponse(BaseModel):
    total_registros: int
    por_pagina: int
    pagina_actual: int
    total_paginas: int
    data: List[FAQCategoryResponse] | List[FAQResponse]