from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from sqlalchemy import func
from models.desaparecidos import Desaparecidos
from schemas.desaparecidos_schema import DesaparecidosCreate, DesaparecidosResponse, PaginatedDesaparecidosResponse
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

# Crear una nueva desaparecidos
@router.post("/desaparecidoss/", response_model=DesaparecidosResponse, tags=["Desaparecidos"])
def create_desaparecidos(desaparecidos: DesaparecidosCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_desaparecidos = Desaparecidos(**desaparecidos.dict())
    db.add(db_desaparecidos)
    db.commit()
    db.refresh(db_desaparecidos)

    # Registrar el log
    log_action(db, action_type="POST", endpoint="/desaparecidoss/", user_id=current_user["sub"], details=str(desaparecidos.dict()))

    return db_desaparecidos

# Obtener lista de desaparecidoss con paginación
@router.get("/desaparecidoss/", response_model=PaginatedDesaparecidosResponse, tags=["Desaparecidos"])
def read_desaparecidoss(skip: int = Query(0, alias="pagina", ge=0), limit: int = Query(5, alias="por_pagina", ge=1), db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    total_registros = db.query(func.count(Desaparecidos.id)).scalar()
    desaparecidoss = db.query(Desaparecidos).offset(skip).limit(limit).all()
    total_paginas = (total_registros + limit - 1) // limit
    pagina_actual = (skip // limit) + 1
    return {
        "total_registros": total_registros,
        "por_pagina": limit,
        "pagina_actual": pagina_actual,
        "total_paginas": total_paginas,
        "data": desaparecidoss
    }

# Obtener desaparecidos por ID
@router.get("/desaparecidoss/{desaparecidos_id}", response_model=DesaparecidosResponse, tags=["Desaparecidos"])
def read_desaparecidos(desaparecidos_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    desaparecidos = db.query(Desaparecidos).filter(Desaparecidos.id == desaparecidos_id).first()
    if desaparecidos is None:
        raise HTTPException(status_code=404, detail="Desaparecidos not found")
    return desaparecidos

# Actualizar desaparecidos por ID
@router.put("/desaparecidoss/{desaparecidos_id}", response_model=DesaparecidosResponse, tags=["Desaparecidos"])
def update_desaparecidos(desaparecidos_id: int, desaparecidos: DesaparecidosCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_desaparecidos = db.query(Desaparecidos).filter(Desaparecidos.id == desaparecidos_id).first()
    if db_desaparecidos is None:
        raise HTTPException(status_code=404, detail="Desaparecidos not found")
    for key, value in desaparecidos.dict().items():
        setattr(db_desaparecidos, key, value)
    db.commit()

    # Registrar el log
    log_action(db, action_type="PUT", endpoint=f"/desaparecidoss/{desaparecidos_id}", user_id=current_user["sub"],
               details=str(desaparecidos.dict()))

    return db_desaparecidos

# Eliminar desaparecidos por ID
@router.delete("/desaparecidoss/{desaparecidos_id}", tags=["Desaparecidos"])
def delete_desaparecidos(desaparecidos_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_desaparecidos = db.query(Desaparecidos).filter(Desaparecidos.id == desaparecidos_id).first()
    if db_desaparecidos is None:
        raise HTTPException(status_code=404, detail="Desaparecidos not found")
    db.delete(db_desaparecidos)
    db.commit()

    # Registrar el log
    log_action(db, action_type="DELETE", endpoint=f"/desaparecidoss/{desaparecidos_id}", user_id=current_user["sub"])

    return {"detail": "Desaparecidos deleted"}
