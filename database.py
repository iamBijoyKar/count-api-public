from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import sqlalchemy as sql

Base = declarative_base()


SQLALCHEMY_DATABASE_URL = "link your database"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL #, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)




