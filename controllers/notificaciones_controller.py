from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from sqlalchemy import func
from models.notificacionespush import NotificacionesPush
from schemas.notificacionespush_schema import NotificacionesPushCreate, NotificacionesPushResponse, PaginatedNotificacionesPushResponse
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

# Crear una nueva notificacionespush
@router.post("/notificacionespushs/", response_model=NotificacionesPushResponse, tags=["NotificacionesPush"])
def create_notificacionespush(notificacionespush: NotificacionesPushCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_notificacionespush = NotificacionesPush(**notificacionespush.dict())
    db.add(db_notificacionespush)
    db.commit()
    db.refresh(db_notificacionespush)

    # Registrar el log
    log_action(db, action_type="POST", endpoint="/notificacionespushs/", user_id=current_user["sub"], details=str(notificacionespush.dict()))

    return db_notificacionespush

# Obtener lista de notificacionespushs con paginación
@router.get("/notificacionespushs/", response_model=PaginatedNotificacionesPushResponse, tags=["NotificacionesPush"])
def read_notificacionespushs(
    pagina: int = Query(1, alias="pagina", ge=1),
    limit: int = Query(5, alias="por_pagina", ge=1),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    total_registros = db.query(func.count(NotificacionesPush.id)).scalar()
    total_paginas = (total_registros + limit - 1) // limit
    offset = (pagina - 1) * limit

    if offset >= total_registros and total_registros != 0:
        raise HTTPException(status_code=404, detail="Página fuera de rango")

    notificacionespushs = db.query(NotificacionesPush).offset(offset).limit(limit).all()

    return {
        "total_registros": total_registros,
        "por_pagina": limit,
        "pagina_actual": pagina,
        "total_paginas": total_paginas,
        "data": notificacionespushs
    }


# Obtener notificacionespush por ID
@router.get("/notificacionespushs/{notificacionespush_id}", response_model=NotificacionesPushResponse, tags=["NotificacionesPush"])
def read_notificacionespush(notificacionespush_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    notificacionespush = db.query(NotificacionesPush).filter(NotificacionesPush.id == notificacionespush_id).first()
    if notificacionespush is None:
        raise HTTPException(status_code=404, detail="NotificacionesPush not found")
    return notificacionespush

# Actualizar notificacionespush por ID
@router.put("/notificacionespushs/{notificacionespush_id}", response_model=NotificacionesPushResponse, tags=["NotificacionesPush"])
def update_notificacionespush(notificacionespush_id: int, notificacionespush: NotificacionesPushCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_notificacionespush = db.query(NotificacionesPush).filter(NotificacionesPush.id == notificacionespush_id).first()
    if db_notificacionespush is None:
        raise HTTPException(status_code=404, detail="NotificacionesPush not found")
    for key, value in notificacionespush.dict().items():
        setattr(db_notificacionespush, key, value)
    db.commit()

    # Registrar el log
    log_action(db, action_type="PUT", endpoint=f"/notificacionespushs/{notificacionespush_id}", user_id=current_user["sub"],
               details=str(notificacionespush.dict()))

    return db_notificacionespush

# Eliminar notificacionespush por ID
@router.delete("/notificacionespushs/{notificacionespush_id}", tags=["NotificacionesPush"])
def delete_notificacionespush(notificacionespush_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_notificacionespush = db.query(NotificacionesPush).filter(NotificacionesPush.id == notificacionespush_id).first()
    if db_notificacionespush is None:
        raise HTTPException(status_code=404, detail="NotificacionesPush not found")
    db.delete(db_notificacionespush)
    db.commit()

    # Registrar el log
    log_action(db, action_type="DELETE", endpoint=f"/notificacionespushs/{notificacionespush_id}", user_id=current_user["sub"])

    return {"detail": "NotificacionesPush deleted"}
