from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://base_unihackz_user:o0Hrk6zKJP2K8CpGtKQfxwrqOSs1ba6r@dpg-ctu4ri9opnds73cj3k1g-a.oregon-postgres.render.com/base_unihackz"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
