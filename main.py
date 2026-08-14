from fastapi import FastAPI
from database import create_db_and_tables
from models import URLs
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield
    
app = FastAPI(lifespan  = lifespan)

@app.get("/")
def root():
    return {"status" : "alive"}