from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import List
class SupportRequestCreate(BaseModel):
    user_id: int
    name: str
    email: str
    subject: str
    message: str
    sent_at: datetime

class SupportRequestResponse(SupportRequestCreate):
    id: int

class PaginatedResponse(BaseModel):
    total_registros: int
    por_pagina: int
    pagina_actual: int
    total_paginas: int
    data: List[SupportRequestResponse]