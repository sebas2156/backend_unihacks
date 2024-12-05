from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from sqlalchemy import func
from models.persona import Persona
from schemas.persona_schema import PersonaCreate, PersonaResponse, PaginatedPersonaResponse
from database import SessionLocal
from .auth import get_current_user  # Importamos la función para obtener el usuario actual

router = APIRouter()

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Crear una nueva persona
@router.post("/personas/", response_model=PersonaResponse, tags=["Persona"])
def create_persona(persona: PersonaCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_persona = Persona(**persona.dict())
    db.add(db_persona)
    db.commit()
    db.refresh(db_persona)
    return db_persona

# Obtener lista de personas con paginación
@router.get("/personas/", response_model=PaginatedPersonaResponse, tags=["Persona"])
def read_personas(skip: int = Query(0, alias="pagina", ge=0), limit: int = Query(5, alias="por_pagina", ge=1), db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    total_registros = db.query(func.count(Persona.id)).scalar()
    personas = db.query(Persona).offset(skip).limit(limit).all()
    total_paginas = (total_registros + limit - 1) // limit
    pagina_actual = (skip // limit) + 1
    return {
        "total_registros": total_registros,
        "por_pagina": limit,
        "pagina_actual": pagina_actual,
        "total_paginas": total_paginas,
        "data": personas
    }

# Obtener persona por ID
@router.get("/personas/{persona_id}", response_model=PersonaResponse, tags=["Persona"])
def read_persona(persona_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    persona = db.query(Persona).filter(Persona.id == persona_id).first()
    if persona is None:
        raise HTTPException(status_code=404, detail="Persona not found")
    return persona

# Actualizar persona por ID
@router.put("/personas/{persona_id}", response_model=PersonaResponse, tags=["Persona"])
def update_persona(persona_id: int, persona: PersonaCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_persona = db.query(Persona).filter(Persona.id == persona_id).first()
    if db_persona is None:
        raise HTTPException(status_code=404, detail="Persona not found")
    for key, value in persona.dict().items():
        setattr(db_persona, key, value)
    db.commit()
    return db_persona

# Eliminar persona por ID
@router.delete("/personas/{persona_id}", tags=["Persona"])
def delete_persona(persona_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_persona = db.query(Persona).filter(Persona.id == persona_id).first()
    if db_persona is None:
        raise HTTPException(status_code=404, detail="Persona not found")
    db.delete(db_persona)
    db.commit()
    return {"detail": "Persona deleted"}
