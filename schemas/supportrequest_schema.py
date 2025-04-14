from pydantic import BaseModel
from typing import Optional, List
import datetime


class SupportRequestCreate(BaseModel):
    user_id: int
    name: str
    email: str
    subject: str
    message: str
    sent_at: datetime.datetime

class SupportRequestResponse(SupportRequestCreate):
    id: int


class PaginatedSupportRequestResponse(BaseModel):
    total_registros: int
    por_pagina: int
    pagina_actual: int
    total_paginas: int
    data: List[SupportRequestResponse]
