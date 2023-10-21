from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#DB Connection
import psycopg2
from psycopg2.extras import RealDictCursor
import time

from .config import settings

# SQLALCHEMY_DATABASE_ULR = 'postgresql://<user>:<password>@<ipaddress/hostname>/<db_name>'
SQLALCHEMY_DATABASE_ULR = f"""postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"""

engine = create_engine(SQLALCHEMY_DATABASE_ULR)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()