from fastapi import FastAPI
from database import create_db_and_tables
from models import URLs
from contextlib import asynccontextmanager
from pydantic import BaseModel, HttpUrl
@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield
    
app = FastAPI(lifespan  = lifespan)

class URLRequest(BaseModel):
    original_url : HttpUrl


@app.get("/")
def root():
    return {"status" : "alive"}


@app.post("/shorten/")
def shorten():

    