from fastapi import FastAPI, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from typing import List

from .database import engine, SessionLocal
from . import models, schemas, crud

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/solicitudes", response_model=schemas.Solicitud)
def crear_solicitud(solicitud: schemas.SolicitudCreate, db: Session = Depends(get_db)):
    return crud.crear_solicitud(db, solicitud)


@app.get("/solicitudes", response_model=List[schemas.Solicitud])
def listar_solicitudes(db: Session = Depends(get_db)):
    return crud.obtener_solicitudes(db)


@app.get("/admin", response_class=HTMLResponse)
def admin(request: Request):
    return templates.TemplateResponse("admin.html", {"request": request})