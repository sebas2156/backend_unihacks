from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy import func
from uuid import UUID
from models.guide import Guide, GuideCategory
from schemas.guide_schema import GuideCreate, GuideResponse, GuideCategoryCreate, GuideCategoryResponse, PaginatedResponse
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

# Rutas CRUD para GuideCategory

@router.post("/guide-categories/", response_model=GuideCategoryResponse, tags=["guide"])
def create_guide_category(category: GuideCategoryCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_category = GuideCategory(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

@router.get("/guide-categories/", response_model=PaginatedResponse, tags=["guide"])
def read_guide_categories(skip: int = Query(0, alias="pagina", ge=0), limit: int = Query(5, alias="por_pagina", ge=1), db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    total_registros = db.query(func.count(GuideCategory.id)).scalar()
    categories = db.query(GuideCategory).offset(skip).limit(limit).all()
    total_paginas = (total_registros + limit - 1) // limit
    pagina_actual = (skip // limit) + 1

    return {
        "total_registros": total_registros,
        "por_pagina": limit,
        "pagina_actual": pagina_actual,
        "total_paginas": total_paginas,
        "data": categories
    }

@router.get("/guide-categories/{category_id}", response_model=GuideCategoryResponse, tags=["guide"])
def read_guide_category(category_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    category = db.query(GuideCategory).filter(GuideCategory.id == category_id).first()
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.put("/guide-categories/{category_id}", response_model=GuideCategoryResponse, tags=["guide"])
def update_guide_category(category_id: int, category: GuideCategoryCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_category = db.query(GuideCategory).filter(GuideCategory.id == category_id).first()
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    for key, value in category.dict().items():
        setattr(db_category, key, value)
    db.commit()
    return db_category

@router.delete("/guide-categories/{category_id}", tags=["guide"])
def delete_guide_category(category_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_category = db.query(GuideCategory).filter(GuideCategory.id == category_id).first()
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(db_category)
    db.commit()
    return {"detail": "Category deleted"}

# Rutas CRUD para Guide

@router.post("/guides/", response_model=GuideResponse, tags=["guide"])
def create_guide(guide: GuideCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_guide = Guide(**guide.dict())
    db.add(db_guide)
    db.commit()
    db.refresh(db_guide)
    return db_guide

@router.get("/guides/", response_model=PaginatedResponse, tags=["guide"])
def read_guides(skip: int = Query(0, alias="pagina", ge=0), limit: int = Query(5, alias="por_pagina", ge=1), db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    total_registros = db.query(func.count(Guide.id)).scalar()
    guides = db.query(Guide).offset(skip).limit(limit).all()
    total_paginas = (total_registros + limit - 1) // limit
    pagina_actual = (skip // limit) + 1

    return {
        "total_registros": total_registros,
        "por_pagina": limit,
        "pagina_actual": pagina_actual,
        "total_paginas": total_paginas,
        "data": guides
    }

@router.get("/guides/{guide_id}", response_model=GuideResponse, tags=["guide"])
def read_guide(guide_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    guide = db.query(Guide).filter(Guide.id == guide_id).first()
    if guide is None:
        raise HTTPException(status_code=404, detail="Guide not found")
    return guide

@router.put("/guides/{guide_id}", response_model=GuideResponse, tags=["guide"])
def update_guide(guide_id: int, guide: GuideCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_guide = db.query(Guide).filter(Guide.id == guide_id).first()
    if db_guide is None:
        raise HTTPException(status_code=404, detail="Guide not found")
    for key, value in guide.dict().items():
        setattr(db_guide, key, value)
    db.commit()
    return db_guide

@router.delete("/guides/{guide_id}", tags=["guide"])
def delete_guide(guide_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_guide = db.query(Guide).filter(Guide.id == guide_id).first()
    if db_guide is None:
        raise HTTPException(status_code=404, detail="Guide not found")
    db.delete(db_guide)
    db.commit()
    return {"detail": "Guide deleted"}
