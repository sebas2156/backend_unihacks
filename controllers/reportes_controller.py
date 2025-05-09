from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy import func
from models.reportes import Reportes  # Suponiendo que el modelo se llama 'Reportes', ajusta el nombre si es necesario.
from schemas.reportes_schema import ReportesCreate, ReportesResponse, PaginatedReportesResponse
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

# Crear un nuevo reportes
@router.post("/reportes/", response_model=ReportesResponse, tags=["Reportes"])
def create_report(report: ReportesCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_report = Reportes(**report.dict())  # Asumiendo que el modelo es Reportes
    db.add(db_report)
    db.commit()
    db.refresh(db_report)

    # Registrar el log
    log_action(db, action_type="POST", endpoint="/reportes/", user_id=current_user["sub"], details=str(report.dict()))

    return db_report

# Obtener lista de reportes con paginación
@router.get("/reportes/", response_model=PaginatedReportesResponse, tags=["Reportes"])
def read_reports(
    pagina: int = Query(1, alias="pagina", ge=1),
    limit: int = Query(5, alias="por_pagina", ge=1),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    total_registros = db.query(func.count(Reportes.id)).scalar()  # Cuenta el número total de registros
    total_paginas = (total_registros + limit - 1) // limit  # Calcula el total de páginas
    offset = (pagina - 1) * limit  # Calcula el offset correcto

    if offset >= total_registros and total_registros != 0:
        raise HTTPException(status_code=404, detail="Página fuera de rango")

    reports = db.query(Reportes).offset(offset).limit(limit).all()  # Obtiene los reportes con paginación

    return {
        "total_registros": total_registros,
        "por_pagina": limit,
        "pagina_actual": pagina,
        "total_paginas": total_paginas,
        "data": reports  # Devuelve los datos paginados
    }


# Obtener reportes por ID
@router.get("/reportes/{report_id}", response_model=ReportesResponse, tags=["Reportes"])
def read_report(report_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    report = db.query(Reportes).filter(Reportes.id == report_id).first()
    if report is None:
        raise HTTPException(status_code=404, detail="Reportes no encontrado")
    return report

# Actualizar reportes por ID
@router.put("/reportes/{report_id}", response_model=ReportesResponse, tags=["Reportes"])
def update_report(report_id: int, report: ReportesCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_report = db.query(Reportes).filter(Reportes.id == report_id).first()
    if db_report is None:
        raise HTTPException(status_code=404, detail="Reportes no encontrado")
    for key, value in report.dict().items():
        setattr(db_report, key, value)  # Actualiza los campos de la base de datos
    db.commit()

    # Registrar el log
    log_action(db, action_type="PUT", endpoint=f"/reportes/{report_id}", user_id=current_user["sub"],
               details=str(report.dict()))

    return db_report

# Eliminar reportes por ID
@router.delete("/reportes/{report_id}", tags=["Reportes"])
def delete_report(report_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_report = db.query(Reportes).filter(Reportes.id == report_id).first()
    if db_report is None:
        raise HTTPException(status_code=404, detail="Reportes no encontrado")
    db.delete(db_report)  # Elimina el reportes de la base de datos
    db.commit()

    # Registrar el log
    log_action(db, action_type="DELETE", endpoint=f"/reportes/{report_id}", user_id=current_user["sub"])

    return {"detail": "Reportes eliminado"}
