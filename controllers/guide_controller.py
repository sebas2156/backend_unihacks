from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy import func
from uuid import UUID
from models.guides import Guide
from models.guidecategories import GuideCategories
from schemas.guides_schema import GuidesCreate, GuidesResponse, PaginatedGuidesResponse
from schemas.guidecategories_schema import GuideCategoriesCreate, GuideCategoriesResponse, PaginatedGuideCategoriesResponse
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

# Rutas CRUD para GuideCategories

@router.post("/Guides-categories/", response_model=GuideCategoriesResponse, tags=["Guides"])
def create_Guides_category(category: GuideCategoriesCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_category = GuideCategories(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)

    # Registrar el log para la acción
    log_action(db, action_type="POST", endpoint="/Guides-categories/", user_id=current_user["sub"],
               details=str(category.dict()))

    return db_category

@router.get("/Guides-categories/", response_model=PaginatedGuideCategoriesResponse, tags=["Guides"])
def read_Guides_categories(skip: int = Query(0, alias="pagina", ge=0), limit: int = Query(5, alias="por_pagina", ge=1), db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    total_registros = db.query(func.count(GuideCategories.id)).scalar()
    categories = db.query(GuideCategories).offset(skip).limit(limit).all()
    total_paginas = (total_registros + limit - 1) // limit
    pagina_actual = (skip // limit) + 1

    return {
        "total_registros": total_registros,
        "por_pagina": limit,
        "pagina_actual": pagina_actual,
        "total_paginas": total_paginas,
        "data": categories
    }

@router.get("/Guides-categories/{category_id}", response_model=GuideCategoriesResponse, tags=["Guides"])
def read_Guides_category(category_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    category = db.query(GuideCategories).filter(GuideCategories.id == category_id).first()
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.put("/Guides-categories/{category_id}", response_model=GuideCategoriesResponse, tags=["Guides"])
def update_Guides_category(category_id: int, category: GuideCategoriesCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_category = db.query(GuideCategories).filter(GuideCategories.id == category_id).first()
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    for key, value in category.dict().items():
        setattr(db_category, key, value)
    db.commit()

    # Registrar el log para la acción
    log_action(db, action_type="PUT", endpoint=f"/Guides-categories/{category_id}", user_id=current_user["sub"],
               details=str(category.dict()))

    return db_category

@router.delete("/Guides-categories/{category_id}", tags=["Guides"])
def delete_Guides_category(category_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_category = db.query(GuideCategories).filter(GuideCategories.id == category_id).first()
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(db_category)
    db.commit()

    # Registrar el log para la acción
    log_action(db, action_type="DELETE", endpoint=f"/Guides-categories/{category_id}", user_id=current_user["sub"])

    return {"detail": "Category deleted"}

# Rutas CRUD para Guides

@router.post("/Guides/", response_model=GuidesResponse, tags=["Guides"])
def create_Guides(Guides: GuidesCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_Guides = Guides(**Guides.dict())
    db.add(db_Guides)
    db.commit()
    db.refresh(db_Guides)

    # Registrar el log para la acción
    log_action(db, action_type="POST", endpoint="/Guides/", user_id=current_user["sub"], details=str(Guides.dict()))

    return db_Guides

@router.get("/Guides/", response_model=PaginatedGuidesResponse, tags=["Guides"])
def read_Guides(skip: int = Query(0, alias="pagina", ge=0), limit: int = Query(5, alias="por_pagina", ge=1), db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    total_registros = db.query(func.count(Guide.id)).scalar()
    Guides = db.query(Guide).offset(skip).limit(limit).all()
    total_paginas = (total_registros + limit - 1) // limit
    pagina_actual = (skip // limit) + 1

    return {
        "total_registros": total_registros,
        "por_pagina": limit,
        "pagina_actual": pagina_actual,
        "total_paginas": total_paginas,
        "data": Guides
    }

@router.get("/Guides/{Guides_id}", response_model=GuidesResponse, tags=["Guides"])
def read_Guides(Guides_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    Guides = db.query(Guide).filter(Guide.id == Guides_id).first()
    if Guides is None:
        raise HTTPException(status_code=404, detail="Guides not found")
    return Guides

@router.put("/Guides/{Guides_id}", response_model=GuidesResponse, tags=["Guides"])
def update_Guides(Guides_id: int, Guides: GuidesCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_Guides = db.query(Guides).filter(Guides.id == Guides_id).first()
    if db_Guides is None:
        raise HTTPException(status_code=404, detail="Guides not found")
    for key, value in Guides.dict().items():
        setattr(db_Guides, key, value)
    db.commit()

    # Registrar el log para la acción
    log_action(db, action_type="PUT", endpoint=f"/Guides/{Guides_id}", user_id=current_user["sub"],
               details=str(Guides.dict()))

    return db_Guides

@router.delete("/Guides/{Guides_id}", tags=["Guides"])
def delete_Guides(Guides_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_Guides = db.query(Guide).filter(Guide.id == Guides_id).first()
    if db_Guides is None:
        raise HTTPException(status_code=404, detail="Guides not found")
    db.delete(db_Guides)
    db.commit()

    # Registrar el log para la acción
    log_action(db, action_type="DELETE", endpoint=f"/Guides/{Guides_id}", user_id=current_user["sub"])

    return {"detail": "Guides deleted"}
