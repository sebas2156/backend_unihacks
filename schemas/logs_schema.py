from pydantic import BaseModel
from typing import Optional, List
import datetime


class LogsCreate(BaseModel):
    action_type: str
    endpoint: str
    user_id: int
    details: str
    timestamp: datetime.datetime = None

class LogsResponse(LogsCreate):
    id: int


class PaginatedLogsResponse(BaseModel):
    total_registros: int
    por_pagina: int
    pagina_actual: int
    total_paginas: int
    data: List[LogsResponse]
