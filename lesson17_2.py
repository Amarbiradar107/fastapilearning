from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, DeclarativeBase

aap = FastAPI()

Database_url = "sqlite:///./test.db"

engine = create_engine(
    Database_url,
    connect_args={"check_same_thread": False}
)

SessionLocal =  sessionmaker(
    bind = engine,
    autocommit = False,
    autoflush=False
)

Base = DeclarativeBase()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)


Base.metadata.create_all(bind=engine)

