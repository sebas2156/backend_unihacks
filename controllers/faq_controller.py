from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import List
from models.faq import FAQCategory, FAQ
from schemas.faq_schema import FAQCategoryCreate, FAQCategoryResponse, FAQCreate, FAQResponse, PaginatedResponse
from database import SessionLocal
from uuid import UUID
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

# CRUD para FAQ Categories

@router.post("/faq-categories/", response_model=FAQCategoryResponse, tags=["FAQ"])
def create_faq_category(category: FAQCategoryCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_category = FAQCategory(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)

    # Registrar el log para la acción
    log_action(db, action_type="POST", endpoint="/faq-categories/", user_id=current_user["id"],
               details=str(category.dict()))

    return db_category

@router.get("/faq-categories/", response_model=PaginatedResponse, tags=["FAQ"])
def read_faq_categories(skip: int = Query(0, alias="pagina", ge=0), limit: int = Query(5, alias="por_pagina", ge=1), db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    total_registros = db.query(func.count(FAQCategory.id)).scalar()
    categories = db.query(FAQCategory).offset(skip).limit(limit).all()
    total_paginas = (total_registros + limit - 1) // limit
    pagina_actual = (skip // limit) + 1

    return {
        "total_registros": total_registros,
        "por_pagina": limit,
        "pagina_actual": pagina_actual,
        "total_paginas": total_paginas,
        "data": categories
    }

@router.get("/faq-categories/{category_id}", response_model=FAQCategoryResponse, tags=["FAQ"])
def read_faq_category(category_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    category = db.query(FAQCategory).filter(FAQCategory.id == category_id).first()
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.put("/faq-categories/{category_id}", response_model=FAQCategoryResponse, tags=["FAQ"])
def update_faq_category(category_id: int, category: FAQCategoryCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_category = db.query(FAQCategory).filter(FAQCategory.id == category_id).first()
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    for key, value in category.dict().items():
        setattr(db_category, key, value)
    db.commit()

    # Registrar el log para la acción
    log_action(db, action_type="PUT", endpoint=f"/faq-categories/{category_id}", user_id=current_user["id"],
               details=str(category.dict()))

    return db_category

@router.delete("/faq-categories/{category_id}", tags=["FAQ"])
def delete_faq_category(category_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_category = db.query(FAQCategory).filter(FAQCategory.id == category_id).first()
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(db_category)
    db.commit()

    # Registrar el log para la acción
    log_action(db, action_type="DELETE", endpoint=f"/faq-categories/{category_id}", user_id=current_user["id"])

    return {"detail": "Category deleted"}

# CRUD para FAQs

@router.post("/faqs/", response_model=FAQResponse, tags=["FAQs"])
def create_faq(faq: FAQCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_faq = FAQ(**faq.dict())
    db.add(db_faq)
    db.commit()
    db.refresh(db_faq)

    # Registrar el log para la acción
    log_action(db, action_type="POST", endpoint="/faqs/", user_id=current_user["id"], details=str(faq.dict()))

    return db_faq

@router.get("/faqs/", response_model=PaginatedResponse, tags=["FAQs"])
def read_faqs(skip: int = Query(0, alias="pagina", ge=0), limit: int = Query(5, alias="por_pagina", ge=1), db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    total_registros = db.query(func.count(FAQ.id)).scalar()
    faqs = db.query(FAQ).offset(skip).limit(limit).all()
    total_paginas = (total_registros + limit - 1) // limit
    pagina_actual = (skip // limit) + 1

    return {
        "total_registros": total_registros,
        "por_pagina": limit,
        "pagina_actual": pagina_actual,
        "total_paginas": total_paginas,
        "data": faqs
    }

@router.get("/faqs/{faq_id}", response_model=FAQResponse, tags=["FAQs"])
def read_faq(faq_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    faq = db.query(FAQ).filter(FAQ.id == faq_id).first()
    if faq is None:
        raise HTTPException(status_code=404, detail="FAQ no encontrada")
    return faq

@router.put("/faqs/{faq_id}", response_model=FAQResponse, tags=["FAQs"])
def update_faq(faq_id: int, faq: FAQCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_faq = db.query(FAQ).filter(FAQ.id == faq_id).first()
    if db_faq is None:
        raise HTTPException(status_code=404, detail="FAQ no encontrada")

    for key, value in faq.dict().items():
        setattr(db_faq, key, value)

    db.commit()
    db.refresh(db_faq)

    # Registrar el log para la acción
    log_action(db, action_type="PUT", endpoint=f"/faqs/{faq_id}", user_id=current_user["id"], details=str(faq.dict()))

    return db_faq

@router.delete("/faqs/{faq_id}", tags=["FAQs"])
def delete_faq(faq_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_faq = db.query(FAQ).filter(FAQ.id == faq_id).first()
    if db_faq is None:
        raise HTTPException(status_code=404, detail="FAQ no encontrada")

    db.delete(db_faq)
    db.commit()

    # Registrar el log para la acción
    log_action(db, action_type="DELETE", endpoint=f"/faqs/{faq_id}", user_id=current_user["id"])

    return {"detail": "FAQ eliminada con éxito"}
