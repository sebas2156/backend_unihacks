from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from sqlalchemy import func
from models.dispositivos import Dispositivos
from schemas.dispositivos_schema import DispositivosCreate, DispositivosResponse, PaginatedDispositivosResponse
from database import SessionLocal
from .auth import get_current_user  # Importamos la función para obtener el usuario actual
from utils.logs import log_action #funcion de logs

router = APIRouter()

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Crear un nuevo dispositivos
@router.post("/dispositivos/", response_model=DispositivosResponse, tags=["Dispositivos"])
def create_dispositivos(dispositivos: DispositivosCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_dispositivos = Dispositivos(**dispositivos.dict())
    db.add(db_dispositivos)
    db.commit()
    db.refresh(db_dispositivos)

    # Registrar el log
    log_action(db, action_type="POST", endpoint="/dispositivos/", user_id=current_user["sub"], details=str(dispositivos.dict()))

    return db_dispositivos

# Obtener lista de dispositivos con paginación
@router.get("/dispositivos/", response_model=PaginatedDispositivosResponse, tags=["Dispositivos"])
def read_dispositivos(skip: int = Query(0, alias="pagina", ge=0), limit: int = Query(5, alias="por_pagina", ge=1), db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    total_registros = db.query(func.count(Dispositivos.codigo_dispositivo)).scalar()
    dispositivos = db.query(Dispositivos).offset(skip).limit(limit).all()
    total_paginas = (total_registros + limit - 1) // limit
    pagina_actual = (skip // limit) + 1
    return {
        "total_registros": total_registros,
        "por_pagina": limit,
        "pagina_actual": pagina_actual,
        "total_paginas": total_paginas,
        "data": dispositivos
    }

# Obtener dispositivos por ID
@router.get("/dispositivos/{dispositivos_id}", response_model=DispositivosResponse, tags=["Dispositivos"])
def read_dispositivos(dispositivos_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    dispositivos = db.query(Dispositivos).filter(Dispositivos.codigo_dispositivo == dispositivos_id).first()
    if dispositivos is None:
        raise HTTPException(status_code=404, detail="Dispositivo not found")
    return dispositivos

# Actualizar dispositivos por ID
@router.put("/dispositivos/{dispositivos_id}", response_model=DispositivosResponse, tags=["Dispositivos"])
def update_dispositivos(dispositivos_id: int, dispositivos: DispositivosCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_dispositivos = db.query(Dispositivos).filter(Dispositivos.codigo_dispositivo == dispositivos_id).first()
    if db_dispositivos is None:
        raise HTTPException(status_code=404, detail="Dispositivo not found")
    for key, value in dispositivos.dict().items():
        setattr(db_dispositivos, key, value)
    db.commit()

    # Registrar el log
    log_action(db, action_type="PUT", endpoint=f"/dispositivos/{dispositivos_id}", user_id=current_user["sub"],
               details=str(dispositivos.dict()))

    return db_dispositivos

# Eliminar dispositivos por ID
@router.delete("/dispositivos/{dispositivos_id}", tags=["Dispositivos"])
def delete_dispositivos(dispositivos_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_dispositivos = db.query(Dispositivos).filter(Dispositivos.codigo_dispositivo == dispositivos_id).first()
    if db_dispositivos is None:
        raise HTTPException(status_code=404, detail="Dispositivo not found")
    db.delete(db_dispositivos)
    db.commit()

    # Registrar el log
    log_action(db, action_type="DELETE", endpoint=f"/dispositivos/{dispositivos_id}", user_id=current_user["sub"])

    return {"detail": "Dispositivo deleted"}
