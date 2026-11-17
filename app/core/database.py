import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy.engine import URL

load_dotenv()

#read environment variables from .env file
DATABASE_URL = URL.create(
    drivername="postgresql+psycopg",
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    database=os.getenv("DB_NAME"),
)

#build the SQLAlchemy engine
engine = create_engine(DATABASE_URL, echo=True)

#create a database session
SessionLocal = sessionmaker(autocommit=False, 
    autoflush=False, 
    bind=engine
)

#create a base class for declarative models
class Base(DeclarativeBase):
    pass

#dependency for database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()