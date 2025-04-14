from fastapi import APIRouter, Depends, HTTPException, Query, Form
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy import func
from uuid import UUID
from models.users import Users
from schemas.users_schema import UsersCreate, UsersResponse, Login, PaginatedUsersResponse
from database import SessionLocal
import bcrypt
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from .auth import get_current_user, create_access_token  # Importamos la función para obtener el usuario actual
from utils.logs import log_action #funcion de logs
from pydantic import BaseModel

router = APIRouter()



# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




# Crear un nuevo usuario
@router.post("/users/", response_model=UsersResponse, tags=["Users"])
def create_users(users: UsersCreate, db: Session = Depends(get_db)):
    # Encriptar la contraseña
    hashed_password = bcrypt.hashpw(users.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    users.password = hashed_password
    db_users = Users(**users.dict())
    db.add(db_users)
    db.commit()
    db.refresh(db_users)

    # Registrar la acción de creación de usuario
    log_action(db, action_type="POST", endpoint="/users/", user_id=db_users.id, details=str(users.dict()))

    return db_users


# Obtener lista de usuarios con paginación
@router.get("/users/", response_model=PaginatedUsersResponse, tags=["Users"])
def read_users(skip: int = Query(0, alias="pagina", ge=0), limit: int = Query(5, alias="por_pagina", ge=1),
               db: Session = Depends(get_db)):
    total_registros = db.query(func.count(Users.id)).scalar()
    users = db.query(Users).offset(skip).limit(limit).all()
    total_paginas = (total_registros + limit - 1) // limit
    pagina_actual = (skip // limit) + 1
    return {
        "total_registros": total_registros,
        "por_pagina": limit,
        "pagina_actual": pagina_actual,
        "total_paginas": total_paginas,
        "data": users
    }

"""""
# Obtener usuario por ID
@router.get("/users/{user_id}", response_model=UsersResponse, tags=["Users"])
def read_users(user_id: int, db: Session = Depends(get_db)):
    users = db.query(Users).filter(Users.id == user_id).first()
    if users is None:
        raise HTTPException(status_code=404, detail="Users not found")
    return users
"""""
@router.get("/v1/user/{user_id}", tags=["Users"])
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.id == user_id).first()

    if user is None:
        raise HTTPException(status_code=404, detail="Users not found")

    return {
        "message": "Users exists",
        "data": {
            "usuarios_id": user.id,
            "nombres": user.name,
            "apellidos": "user.apellido",
            "usuario": "user.usuario",
            "email": user.email,
            "estado": int(user.status),
            "role": str(user.role),
            "image": None
        }
    }
# Actualizar usuario por ID
@router.put("/users/{user_id}", response_model=UsersResponse, tags=["Users"])
def update_users(user_id: int, users: UsersCreate, db: Session = Depends(get_db)):
    db_users = db.query(Users).filter(Users.id == user_id).first()
    if db_users is None:
        raise HTTPException(status_code=404, detail="Users not found")
    for key, value in users.dict().items():
        setattr(db_users, key, value)
    db.commit()

    # Registrar la acción de actualización de usuario
    log_action(db, action_type="PUT", endpoint=f"/users/{user_id}", user_id=db_users.id, details=str(users.dict()))

    return db_users


# Eliminar usuario por ID
@router.delete("/users/{users_id}", tags=["Users"])
def delete_users(user_id: int, db: Session = Depends(get_db)):
    db_users = db.query(Users).filter(Users.id == user_id).first()
    if db_users is None:
        raise HTTPException(status_code=404, detail="Users not found")
    db.delete(db_users)
    db.commit()

    # Registrar la acción de eliminación de usuario
    log_action(db, action_type="DELETE", endpoint=f"/users/{user_id}", user_id=user_id, details=db_users.email)

    return {"detail": "Users deleted"}


# Ruta de login, genera un JWT cuando el usuario inicia sesión
@router.post("/login/", tags=["Users"])
def login(
    username: str = Form(...),  # Recibe el email desde el formulario
    password: str = Form(...),  # Recibe la contraseña desde el formulario
    db: Session = Depends(get_db)
):
    # Busca al usuario en la base de datos por su email
    users = db.query(Users).filter(Users.email == username).first()

    # Verifica si el usuario existe y la contraseña es correcta
    if not users or not bcrypt.checkpw(password.encode('utf-8'), users.password.encode('utf-8')):
        raise HTTPException(status_code=400, detail="Correo electrónico o contraseña incorrectos")

    # Crear el JWT (token de acceso)
    access_token = create_access_token(data={"sub": str(users.id)})

    # Log de intento de login exitoso (esto es opcional)
    log_action(db, action_type="LOGIN_SUCCESS", endpoint="/login/", user_id=users.id,
               details=f"Email: {username} - Inicio de sesión exitoso")

    # Respuesta con el token y los detalles del usuario
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": users.id,
        "email": users.email
    }


class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/v1/user/login", tags=["Users"])
def login(request: LoginRequest, db: Session = Depends(get_db)):
    # Buscar usuario por email
    users = db.query(Users).filter(Users.email == request.email).first()

    # Validación de existencia y contraseña
    if not users or not bcrypt.checkpw(request.password.encode('utf-8'), users.password.encode('utf-8')):
        raise HTTPException(status_code=401, detail="Correo electrónico o contraseña incorrectos")

    # Datos para el token
    token_data = {
        "id": str(users.id),
        "email": users.email,
        "role": str(users.role)
    }
    access_token = create_access_token(data=token_data)

    # Respuesta
    return {
        "message": "Inicio de sesión exitoso",
        "user": {
            "id": str(users.id),
            "email": users.email,
            "role": str(users.role)
        },
        "token": access_token
    }