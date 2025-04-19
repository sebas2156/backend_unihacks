import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Obtener la URL de la base de datos desde la variable de entorno
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# Configurar la base de datos
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()