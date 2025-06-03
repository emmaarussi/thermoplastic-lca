from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base  # Import your models here

DATABASE_URL = 'postgresql://postgres:postgres@localhost/thermoplastic_lca'
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

# Add more routes and logic as needed
