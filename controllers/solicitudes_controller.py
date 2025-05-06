from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from sqlalchemy import func
from models.solicitudesayuda import SolicitudesAyuda
from schemas.solicitudesayuda_schema import SolicitudesAyudaCreate, SolicitudesAyudaResponse, PaginatedSolicitudesAyudaResponse
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
@router.post("/solicitudess/", response_model=SolicitudesAyudaResponse, tags=["SolicitudesAyuda"])
def create_solicitudes(solicitudes: SolicitudesAyudaCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_solicitudes = SolicitudesAyuda(**solicitudes.dict())
    db.add(db_solicitudes)
    db.commit()
    db.refresh(db_solicitudes)

    # Registrar el log
    log_action(db, action_type="POST", endpoint="/solicitudess/", user_id=current_user["sub"], details=str(solicitudes.dict()))

    return db_solicitudes

# Obtener lista de solicitudess con paginación
@router.get("/solicitudess/", response_model=PaginatedSolicitudesAyudaResponse, tags=["SolicitudesAyuda"])
def read_solicitudess(
    pagina: int = Query(1, alias="pagina", ge=1),
    limit: int = Query(5, alias="por_pagina", ge=1),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    total_registros = db.query(func.count(SolicitudesAyuda.codigo_panico)).scalar()  # Cuenta el número total de registros
    total_paginas = (total_registros + limit - 1) // limit  # Calcula el total de páginas
    offset = (pagina - 1) * limit  # Calcula el offset correcto

    if offset >= total_registros and total_registros != 0:
        raise HTTPException(status_code=404, detail="Página fuera de rango")

    solicitudess = db.query(SolicitudesAyuda).offset(offset).limit(limit).all()  # Obtiene las solicitudes con paginación

    return {
        "total_registros": total_registros,
        "por_pagina": limit,
        "pagina_actual": pagina,
        "total_paginas": total_paginas,
        "data": solicitudess  # Devuelve los datos paginados
    }


# Obtener solicitudes por ID
@router.get("/solicitudess/{solicitudes_id}", response_model=SolicitudesAyudaResponse, tags=["SolicitudesAyuda"])
def read_solicitudes(solicitudes_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    solicitudes = db.query(SolicitudesAyuda).filter(SolicitudesAyuda.codigo_panico == solicitudes_id).first()
    if solicitudes is None:
        raise HTTPException(status_code=404, detail="SolicitudesAyuda not found")
    return solicitudes

# Actualizar solicitudes por ID
@router.put("/solicitudess/{solicitudes_id}", response_model=SolicitudesAyudaResponse, tags=["SolicitudesAyuda"])
def update_solicitudes(solicitudes_id: int, solicitudes: SolicitudesAyudaCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_solicitudes = db.query(SolicitudesAyuda).filter(SolicitudesAyuda.codigo_panico == solicitudes_id).first()
    if db_solicitudes is None:
        raise HTTPException(status_code=404, detail="SolicitudesAyuda not found")
    for key, value in solicitudes.dict().items():
        setattr(db_solicitudes, key, value)
    db.commit()

    # Registrar el log
    log_action(db, action_type="PUT", endpoint=f"/solicitudess/{solicitudes_id}", user_id=current_user["sub"],
               details=str(solicitudes.dict()))

    return db_solicitudes

# Eliminar solicitudes por ID
@router.delete("/solicitudess/{solicitudes_id}", tags=["SolicitudesAyuda"])
def delete_solicitudes(solicitudes_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_solicitudes = db.query(SolicitudesAyuda).filter(SolicitudesAyuda.codigo_panico == solicitudes_id).first()
    if db_solicitudes is None:
        raise HTTPException(status_code=404, detail="SolicitudesAyuda not found")
    db.delete(db_solicitudes)
    db.commit()

    # Registrar el log
    log_action(db, action_type="DELETE", endpoint=f"/solicitudess/{solicitudes_id}", user_id=current_user["sub"])

    return {"detail": "SolicitudesAyuda deleted"}
