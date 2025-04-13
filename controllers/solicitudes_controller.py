from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from sqlalchemy import func
from models.solicitudes_ayuda import Solicitudes
from schemas.solicitudes_ayuda_schema import SolicitudesCreate, SolicitudesResponse, PaginatedSolicitudesResponse
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

# Crear un nuevo solicitudes
@router.post("/solicitudess/", response_model=SolicitudesResponse, tags=["Solicitudes"])
def create_solicitudes(solicitudes: SolicitudesCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_solicitudes = Solicitudes(**solicitudes.dict())
    db.add(db_solicitudes)
    db.commit()
    db.refresh(db_solicitudes)

    # Registrar el log
    log_action(db, action_type="POST", endpoint="/solicitudess/", user_id=current_user["sub"], details=str(solicitudes.dict()))

    return db_solicitudes

# Obtener lista de solicitudess con paginación
@router.get("/solicitudess/", response_model=PaginatedSolicitudesResponse, tags=["Solicitudes"])
def read_solicitudess(skip: int = Query(0, alias="pagina", ge=0), limit: int = Query(5, alias="por_pagina", ge=1), db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    total_registros = db.query(func.count(Solicitudes.codigo_panico)).scalar()
    solicitudess = db.query(Solicitudes).offset(skip).limit(limit).all()
    total_paginas = (total_registros + limit - 1) // limit
    pagina_actual = (skip // limit) + 1
    return {
        "total_registros": total_registros,
        "por_pagina": limit,
        "pagina_actual": pagina_actual,
        "total_paginas": total_paginas,
        "data": solicitudess
    }

# Obtener solicitudes por ID
@router.get("/solicitudess/{solicitudes_id}", response_model=SolicitudesResponse, tags=["Solicitudes"])
def read_solicitudes(solicitudes_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    solicitudes = db.query(Solicitudes).filter(Solicitudes.codigo_panico == solicitudes_id).first()
    if solicitudes is None:
        raise HTTPException(status_code=404, detail="Solicitudes not found")
    return solicitudes

# Actualizar solicitudes por ID
@router.put("/solicitudess/{solicitudes_id}", response_model=SolicitudesResponse, tags=["Solicitudes"])
def update_solicitudes(solicitudes_id: int, solicitudes: SolicitudesCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_solicitudes = db.query(Solicitudes).filter(Solicitudes.codigo_panico == solicitudes_id).first()
    if db_solicitudes is None:
        raise HTTPException(status_code=404, detail="Solicitudes not found")
    for key, value in solicitudes.dict().items():
        setattr(db_solicitudes, key, value)
    db.commit()

    # Registrar el log
    log_action(db, action_type="PUT", endpoint=f"/solicitudess/{solicitudes_id}", user_id=current_user["sub"],
               details=str(solicitudes.dict()))

    return db_solicitudes

# Eliminar solicitudes por ID
@router.delete("/solicitudess/{solicitudes_id}", tags=["Solicitudes"])
def delete_solicitudes(solicitudes_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_solicitudes = db.query(Solicitudes).filter(Solicitudes.codigo_panico == solicitudes_id).first()
    if db_solicitudes is None:
        raise HTTPException(status_code=404, detail="Solicitudes not found")
    db.delete(db_solicitudes)
    db.commit()

    # Registrar el log
    log_action(db, action_type="DELETE", endpoint=f"/solicitudess/{solicitudes_id}", user_id=current_user["sub"])

    return {"detail": "Solicitudes deleted"}
