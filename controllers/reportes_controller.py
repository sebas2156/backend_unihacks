from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy import func
from models.reportes import Reporte  # Suponiendo que el modelo se llama 'Reporte', ajusta el nombre si es necesario.
from schemas.reporte_schema import ReporteCreate, ReporteResponse, PaginatedReporteResponse
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

# Crear un nuevo reporte
@router.post("/reportes/", response_model=ReporteResponse, tags=["Reportes"])
def create_report(report: ReporteCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_report = Reporte(**report.dict())  # Asumiendo que el modelo es Reporte
    db.add(db_report)
    db.commit()
    db.refresh(db_report)

    # Registrar el log
    log_action(db, action_type="POST", endpoint="/reportes/", user_id=current_user["id"], details=str(report.dict()))

    return db_report

# Obtener lista de reportes con paginación
@router.get("/reportes/", response_model=PaginatedReporteResponse, tags=["Reportes"])
def read_reports(skip: int = Query(0, alias="pagina", ge=0), limit: int = Query(5, alias="por_pagina", ge=1), db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    total_registros = db.query(func.count(Reporte.id)).scalar()  # Cuenta el número total de registros
    reports = db.query(Reporte).offset(skip).limit(limit).all()  # Obtiene los reportes con paginación
    total_paginas = (total_registros + limit - 1) // limit  # Calcula el total de páginas
    pagina_actual = (skip // limit) + 1  # Calcula la página actual
    return {
        "total_registros": total_registros,
        "por_pagina": limit,
        "pagina_actual": pagina_actual,
        "total_paginas": total_paginas,
        "data": reports  # Devuelve los datos paginados
    }

# Obtener reporte por ID
@router.get("/reportes/{report_id}", response_model=ReporteResponse, tags=["Reportes"])
def read_report(report_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    report = db.query(Reporte).filter(Reporte.id == report_id).first()
    if report is None:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")
    return report

# Actualizar reporte por ID
@router.put("/reportes/{report_id}", response_model=ReporteResponse, tags=["Reportes"])
def update_report(report_id: int, report: ReporteCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_report = db.query(Reporte).filter(Reporte.id == report_id).first()
    if db_report is None:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")
    for key, value in report.dict().items():
        setattr(db_report, key, value)  # Actualiza los campos de la base de datos
    db.commit()

    # Registrar el log
    log_action(db, action_type="PUT", endpoint=f"/reportes/{report_id}", user_id=current_user["id"],
               details=str(report.dict()))

    return db_report

# Eliminar reporte por ID
@router.delete("/reportes/{report_id}", tags=["Reportes"])
def delete_report(report_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_report = db.query(Reporte).filter(Reporte.id == report_id).first()
    if db_report is None:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")
    db.delete(db_report)  # Elimina el reporte de la base de datos
    db.commit()

    # Registrar el log
    log_action(db, action_type="DELETE", endpoint=f"/reportes/{report_id}", user_id=current_user["id"])

    return {"detail": "Reporte eliminado"}
