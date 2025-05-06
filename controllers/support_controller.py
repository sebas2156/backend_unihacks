from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from sqlalchemy import func
from models.supportrequest import SupportRequest
from schemas.supportrequest_schema import SupportRequestCreate, SupportRequestResponse, PaginatedSupportRequestResponse
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

# Rutas protegidas que requieren que el usuario esté autenticado

@router.post("/support-requests/", response_model=SupportRequestResponse, tags=["Support Request"])
def create_support_request(request: SupportRequestCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    # 'current_user' es el resultado de 'get_current_user', que contiene los datos del usuario autenticado
    db_request = SupportRequest(**request.dict())
    db.add(db_request)
    db.commit()
    db.refresh(db_request)

    # Registrar el log para la acción
    log_action(db, action_type="POST", endpoint="/support-requests/", user_id=current_user["sub"],
               details=str(request.dict()))

    return db_request

@router.get("/support-requests/", response_model=PaginatedSupportRequestResponse, tags=["Support Request"])
def read_support_requests(
    pagina: int = Query(1, alias="pagina", ge=1),
    limit: int = Query(5, alias="por_pagina", ge=1),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    total_registros = db.query(func.count(SupportRequest.id)).scalar()  # Cuenta el número total de registros
    total_paginas = (total_registros + limit - 1) // limit  # Calcula el total de páginas
    offset = (pagina - 1) * limit  # Calcula el offset correcto

    if offset >= total_registros and total_registros != 0:
        raise HTTPException(status_code=404, detail="Página fuera de rango")

    requests = db.query(SupportRequest).offset(offset).limit(limit).all()  # Obtiene las solicitudes con paginación

    return {
        "total_registros": total_registros,
        "por_pagina": limit,
        "pagina_actual": pagina,
        "total_paginas": total_paginas,
        "data": requests  # Devuelve los datos paginados
    }


@router.get("/support-requests/{request_id}", response_model=SupportRequestResponse, tags=["Support Request"])
def read_support_request(request_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    request = db.query(SupportRequest).filter(SupportRequest.id == request_id).first()
    if request is None:
        raise HTTPException(status_code=404, detail="Request not found")
    return request

@router.put("/support-requests/{request_id}", response_model=SupportRequestResponse, tags=["Support Request"])
def update_support_request(request_id: int, request: SupportRequestCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_request = db.query(SupportRequest).filter(SupportRequest.id == request_id).first()
    if db_request is None:
        raise HTTPException(status_code=404, detail="Request not found")
    for key, value in request.dict().items():
        setattr(db_request, key, value)
    db.commit()

    # Registrar el log para la acción
    log_action(db, action_type="PUT", endpoint=f"/support-requests/{request_id}", user_id=current_user["sub"],
               details=str(request.dict()))

    return db_request

@router.delete("/support-requests/{request_id}", tags=["Support Request"])
def delete_support_request(request_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_request = db.query(SupportRequest).filter(SupportRequest.id == request_id).first()
    if db_request is None:
        raise HTTPException(status_code=404, detail="Request not found")
    db.delete(db_request)
    db.commit()

    # Registrar el log para la acción
    log_action(db, action_type="DELETE", endpoint=f"/support-requests/{request_id}", user_id=current_user["sub"])

    return {"detail": "Request deleted"}
