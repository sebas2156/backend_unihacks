from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://baseunihackz_1vv2_user:hcmxmSC7KMwU9z67SXKdbEiiHio6UpE1@dpg-ct947be8ii6s73fq01j0-a.oregon-postgres.render.com/baseunihackz_1vv2"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
