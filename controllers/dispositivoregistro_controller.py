from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from sqlalchemy import func
from models.dispositivoregistro import DispositivoRegistro
from schemas.dispositivoregistro_schema import DispositivoRegistroCreate, DispositivoRegistroResponse, PaginatedDispositivoRegistroResponse
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

# Crear una nueva dispositivoregistro
@router.post("/dispositivoregistros/", response_model=DispositivoRegistroResponse, tags=["Dispositivo Registro"])
def create_dispositivoregistro(dispositivoregistro: DispositivoRegistroCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_dispositivoregistro = DispositivoRegistro(**dispositivoregistro.dict())
    db.add(db_dispositivoregistro)
    db.commit()
    db.refresh(db_dispositivoregistro)

    # Registrar el log
    log_action(db, action_type="POST", endpoint="/dispositivoregistros/", user_id=current_user["sub"], details=str(dispositivoregistro.dict()))

    return db_dispositivoregistro

# Obtener lista de dispositivoregistros con paginación
@router.get("/dispositivoregistros/", response_model=PaginatedDispositivoRegistroResponse, tags=["Dispositivo Registro"])
def read_dispositivoregistros(
    pagina: int = Query(1, alias="pagina", ge=1),
    limit: int = Query(5, alias="por_pagina", ge=1),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    total_registros = db.query(func.count(DispositivoRegistro.id)).scalar()
    total_paginas = (total_registros + limit - 1) // limit
    offset = (pagina - 1) * limit

    if offset >= total_registros and total_registros != 0:
        raise HTTPException(status_code=404, detail="Página fuera de rango")

    dispositivoregistros = db.query(DispositivoRegistro).offset(offset).limit(limit).all()

    return {
        "total_registros": total_registros,
        "por_pagina": limit,
        "pagina_actual": pagina,
        "total_paginas": total_paginas,
        "data": dispositivoregistros
    }


# Obtener dispositivoregistro por ID
@router.get("/dispositivoregistros/{dispositivoregistro_id}", response_model=DispositivoRegistroResponse, tags=["Dispositivo Registro"])
def read_dispositivoregistro(dispositivoregistro_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    dispositivoregistro = db.query(DispositivoRegistro).filter(DispositivoRegistro.id == dispositivoregistro_id).first()
    if dispositivoregistro is None:
        raise HTTPException(status_code=404, detail="DispositivoRegistro not found")
    return dispositivoregistro

# Actualizar dispositivoregistro por ID
@router.put("/dispositivoregistros/{dispositivoregistro_id}", response_model=DispositivoRegistroResponse, tags=["Dispositivo Registro"])
def update_dispositivoregistro(dispositivoregistro_id: int, dispositivoregistro: DispositivoRegistroCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_dispositivoregistro = db.query(DispositivoRegistro).filter(DispositivoRegistro.id == dispositivoregistro_id).first()
    if db_dispositivoregistro is None:
        raise HTTPException(status_code=404, detail="DispositivoRegistro not found")
    for key, value in dispositivoregistro.dict().items():
        setattr(db_dispositivoregistro, key, value)
    db.commit()

    # Registrar el log
    log_action(db, action_type="PUT", endpoint=f"/dispositivoregistros/{dispositivoregistro_id}", user_id=current_user["sub"],
               details=str(dispositivoregistro.dict()))

    return db_dispositivoregistro

# Eliminar dispositivoregistro por ID
@router.delete("/dispositivoregistros/{dispositivoregistro_id}", tags=["Dispositivo Registro"])
def delete_dispositivoregistro(dispositivoregistro_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_dispositivoregistro = db.query(DispositivoRegistro).filter(DispositivoRegistro.id == dispositivoregistro_id).first()
    if db_dispositivoregistro is None:
        raise HTTPException(status_code=404, detail="DispositivoRegistro not found")
    db.delete(db_dispositivoregistro)
    db.commit()

    # Registrar el log
    log_action(db, action_type="DELETE", endpoint=f"/dispositivoregistros/{dispositivoregistro_id}", user_id=current_user["sub"])

    return {"detail": "DispositivoRegistro deleted"}
