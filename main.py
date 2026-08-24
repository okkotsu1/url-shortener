from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from database import create_db_and_tables
from models import URLs
from sqlmodel import select
from contextlib import asynccontextmanager
from pydantic import BaseModel, HttpUrl
from database import SessionDep 
from utils import generate_short_code
from cache import get_cached_url, set_cached_url

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


@app.post("/shorten/", status_code=201)
def shorten(request : URLRequest, db : SessionDep):
    url = URLs(original_url = str(request.original_url), short_code = generate_short_code(6))
    db.add(url)
    db.commit()
    db.refresh(url)
    return{
        "short_code":url.short_code,
        "short_url":"http://localhost:8000/" + url.short_code 
    }

@app.get("/{short_code}", status_code = 302)
def redirect(short_code : str, db : SessionDep):
    cached_url = get_cached_url(short_code)
    if cached_url != None:
        return RedirectResponse(url = cached_url)
    statement = select(URLs).where(URLs.short_code == short_code)
    result = db.exec(statement).first()
    if result == None:
        raise HTTPException(
            status_code = 404,
            detail = f"{short_code} not found."
        )
    else:
        set_cached_url(result.short_code, result.original_url)
        return RedirectResponse(url = result.original_url)


    