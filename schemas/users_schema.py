from pydantic import BaseModel
from typing import Optional, List
import datetime


class UsersCreate(BaseModel):
    codigo_persona: str
    email: str
    avatar_imagen: str
    status: str
    role: str
    password: str
    numero: str = None
    token_firebase: str = None
    linea_telefonica: str = None
    username: str = None
    name: str = None

class UsersResponse(UsersCreate):
    id: int

class Login(BaseModel):
    email: str
    password: str


class PaginatedUsersResponse(BaseModel):
    total_registros: int
    por_pagina: int
    pagina_actual: int
    total_paginas: int
    data: List[UsersResponse]
