from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

SQLITE_DATABASE_URL_DEFAULT = "sqlite:///demo.db"
sql_connection_string = SQLITE_DATABASE_URL_DEFAULT
if os.environ.get('TESTING', None):
    sql_connection_string = os.environ['SQLITE_TEST']

engine = create_engine(sql_connection_string, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
