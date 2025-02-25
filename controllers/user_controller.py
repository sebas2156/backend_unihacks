from fastapi import APIRouter, Depends, HTTPException, Query, Form
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy import func
from uuid import UUID
from models.user import User
from schemas.user_schema import UserCreate, UserResponse, Login, PaginatedResponse
from database import SessionLocal
import bcrypt
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from .auth import get_current_user, create_access_token  # Importamos la función para obtener el usuario actual
from utils.logs import log_action #funcion de logs

router = APIRouter()



# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




# Crear un nuevo usuario
@router.post("/users/", response_model=UserResponse, tags=["User"])
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Encriptar la contraseña
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    user.password = hashed_password
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # Registrar la acción de creación de usuario
    log_action(db, action_type="POST", endpoint="/users/", user_id=db_user.id, details=str(user.dict()))

    return db_user


# Obtener lista de usuarios con paginación
@router.get("/users/", response_model=PaginatedResponse, tags=["User"])
def read_users(skip: int = Query(0, alias="pagina", ge=0), limit: int = Query(5, alias="por_pagina", ge=1),
               db: Session = Depends(get_db)):
    total_registros = db.query(func.count(User.id)).scalar()
    users = db.query(User).offset(skip).limit(limit).all()
    total_paginas = (total_registros + limit - 1) // limit
    pagina_actual = (skip // limit) + 1
    return {
        "total_registros": total_registros,
        "por_pagina": limit,
        "pagina_actual": pagina_actual,
        "total_paginas": total_paginas,
        "data": users
    }


# Obtener usuario por ID
@router.get("/users/{user_id}", response_model=UserResponse, tags=["User"])
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# Actualizar usuario por ID
@router.put("/users/{user_id}", response_model=UserResponse, tags=["User"])
def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    for key, value in user.dict().items():
        setattr(db_user, key, value)
    db.commit()

    # Registrar la acción de actualización de usuario
    log_action(db, action_type="PUT", endpoint=f"/users/{user_id}", user_id=db_user.id, details=str(user.dict()))

    return db_user


# Eliminar usuario por ID
@router.delete("/users/{user_id}", tags=["User"])
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()

    # Registrar la acción de eliminación de usuario
    log_action(db, action_type="DELETE", endpoint=f"/users/{user_id}", user_id=user_id, details=db_user.email)

    return {"detail": "User deleted"}


# Ruta de login, genera un JWT cuando el usuario inicia sesión
@router.post("/login/", tags=["User"])
def login(
    username: str = Form(...),  # Recibe el email desde el formulario
    password: str = Form(...),  # Recibe la contraseña desde el formulario
    db: Session = Depends(get_db)
):
    # Busca al usuario en la base de datos por su email
    user = db.query(User).filter(User.email == username).first()

    # Verifica si el usuario existe y la contraseña es correcta
    if not user or not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        raise HTTPException(status_code=400, detail="Correo electrónico o contraseña incorrectos")

    # Crear el JWT (token de acceso)
    access_token = create_access_token(data={"sub": str(user.id)})

    # Log de intento de login exitoso (esto es opcional)
    log_action(db, action_type="LOGIN_SUCCESS", endpoint="/login/", user_id=user.id,
               details=f"Email: {username} - Inicio de sesión exitoso")

    # Respuesta con el token y los detalles del usuario
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id,
        "email": user.email
    }