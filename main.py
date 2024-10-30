from fastapi import FastAPI
from controllers.faq_controller import router as faq_router
from controllers.guide_controller import router as guide_router
from controllers.support_controller import router as support_router
from controllers.user_controller import router as user_router
from database import Base, engine

app = FastAPI()

# Crea las tablas
Base.metadata.create_all(bind=engine)

# Incluir routers
app.include_router(faq_router, prefix="/api", tags=["FAQ"])
app.include_router(guide_router, prefix="/api", tags=["Guide"])
app.include_router(support_router, prefix="/api", tags=["Support"])
app.include_router(user_router, prefix="/api", tags=["User"])
