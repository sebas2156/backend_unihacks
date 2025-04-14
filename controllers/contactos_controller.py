from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from sqlalchemy import func
from models.contactoemergencia import ContactoEmergencia
from schemas.contactoemergencia_schema import ContactoEmergenciaCreate, ContactoEmergenciaResponse, PaginatedContactoEmergenciaResponse
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

# Crear un nuevo contactos
@router.post("/contactoss/", response_model=ContactoEmergenciaResponse, tags=["ContactoEmergencia"])
def create_contactos(contactos: ContactoEmergenciaCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_contactos = ContactoEmergencia(**contactos.dict())
    db.add(db_contactos)
    db.commit()
    db.refresh(db_contactos)

    # Registrar el log
    log_action(db, action_type="POST", endpoint="/contactoss/", user_id=current_user["sub"], details=str(contactos.dict()))

    return db_contactos

# Obtener lista de contactoss con paginación
@router.get("/contactoss/", response_model=PaginatedContactoEmergenciaResponse, tags=["ContactoEmergencia"])
def read_contactoss(skip: int = Query(0, alias="pagina", ge=0), limit: int = Query(5, alias="por_pagina", ge=1), db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    total_registros = db.query(func.count(ContactoEmergencia.id)).scalar()
    contactoss = db.query(ContactoEmergencia).offset(skip).limit(limit).all()
    total_paginas = (total_registros + limit - 1) // limit
    pagina_actual = (skip // limit) + 1
    return {
        "total_registros": total_registros,
        "por_pagina": limit,
        "pagina_actual": pagina_actual,
        "total_paginas": total_paginas,
        "data": contactoss
    }

# Obtener contactos por ID
@router.get("/contactoss/{contactos_id}", response_model=ContactoEmergenciaResponse, tags=["ContactoEmergencia"])
def read_contactos(contactos_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    contactos = db.query(ContactoEmergencia).filter(ContactoEmergencia.id == contactos_id).first()
    if contactos is None:
        raise HTTPException(status_code=404, detail="ContactoEmergencia not found")
    return contactos

# Actualizar contactos por ID
@router.put("/contactoss/{contactos_id}", response_model=ContactoEmergenciaResponse, tags=["ContactoEmergencia"])
def update_contactos(contactos_id: int, contactos: ContactoEmergenciaCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_contactos = db.query(ContactoEmergencia).filter(ContactoEmergencia.id == contactos_id).first()
    if db_contactos is None:
        raise HTTPException(status_code=404, detail="ContactoEmergencia not found")
    for key, value in contactos.dict().items():
        setattr(db_contactos, key, value)
    db.commit()

    # Registrar el log
    log_action(db, action_type="PUT", endpoint=f"/contactoss/{contactos_id}", user_id=current_user["sub"],
               details=str(contactos.dict()))

    return db_contactos

# Eliminar contactos por ID
@router.delete("/contactoss/{contactos_id}", tags=["ContactoEmergencia"])
def delete_contactos(contactos_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_contactos = db.query(ContactoEmergencia).filter(ContactoEmergencia.id == contactos_id).first()
    if db_contactos is None:
        raise HTTPException(status_code=404, detail="ContactoEmergencia not found")
    db.delete(db_contactos)
    db.commit()

    # Registrar el log
    log_action(db, action_type="DELETE", endpoint=f"/contactoss/{contactos_id}", user_id=current_user["sub"])

    return {"detail": "ContactoEmergencia deleted"}
