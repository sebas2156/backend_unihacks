from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers.faq_controller import router as faq_router
from controllers.guide_controller import router as guide_router
from controllers.support_controller import router as support_router
from controllers.user_controller import router as user_router
from controllers.personas_controller import router as personas_router
from controllers.reportes_controller import router as reportes_router
from controllers.contactos_controller import router as contactos_router
from controllers.solicitudes_controller import router as solicitudes_router
from controllers.dispositivos_controller import router as dispositivo_router
from controllers.notificaciones_controller import router as notificaciones_router
from controllers.dispositivoregistro_controller import router as dispositivo_registro_router
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
app.include_router(faq_router, prefix="/api")
app.include_router(guide_router, prefix="/api", tags=["Guides"])
app.include_router(support_router, prefix="/api", tags=["Support Request"])
app.include_router(user_router, prefix="/api", tags=["Users"])
app.include_router(personas_router, prefix="/api", tags=["Desaparecidos"])
app.include_router(reportes_router, prefix="/api", tags=["Reportes"])
app.include_router(contactos_router, prefix="/api", tags=["ContactoEmergencia"])
app.include_router(solicitudes_router, prefix="/api", tags=["SolicitudesAyuda"])
app.include_router(dispositivo_router, prefix="/api", tags=["Dispositivos"])
app.include_router(notificaciones_router, prefix="/api", tags=["NotificacionesPush"])
app.include_router(dispositivo_registro_router, prefix="/api", tags=["Dispositivo Registro"])