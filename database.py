from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://baseunihackz_user:1jE4VgmfimhCMNQQeBJfoIhc3ajJNTR5@pg-cshbag56l47c73adrfu0-a.oregon-postgres.render.com:5432/baseunihackz"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
