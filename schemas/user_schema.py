from pydantic import BaseModel
from uuid import UUID
from typing import List

class UserCreate(BaseModel):
    name: str
    password: str
    email: str
    avatar: str
    status: str
    role: str
    numero : int
class UserResponse(UserCreate):
    id: int

class Login(BaseModel):
    email: str
    password: str

class PaginatedResponse(BaseModel):
    total_registros: int
    por_pagina: int
    pagina_actual: int
    total_paginas: int
    data: List[UserResponse]