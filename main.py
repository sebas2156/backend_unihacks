from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers.faq_controller import router as faq_router
from controllers.guide_controller import router as guide_router
from controllers.support_controller import router as support_router
from controllers.user_controller import router as user_router
from controllers.personas_controller import router as personas_router
from controllers.reportes_controller import router as reportes_router
from controllers.contactos_controller import router as contactos_router
from database import Base, engine

app = FastAPI()

# Configurar CORS
origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos los encabezados
)

# Crea las tablas
Base.metadata.create_all(bind=engine)

# Incluir routers
app.include_router(faq_router, prefix="/api", tags=["FAQ"])
app.include_router(guide_router, prefix="/api", tags=["Guide"])
app.include_router(support_router, prefix="/api", tags=["Support"])
app.include_router(user_router, prefix="/api", tags=["User"])
app.include_router(personas_router, prefix="/api", tags=["Personas"])
app.include_router(reportes_router, prefix="/api", tags=["Reports"])
app.include_router(contactos_router, prefix="/api", tags=["Contactos"])
