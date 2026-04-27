import os
from dotenv import load_dotenv
from datetime import timedelta

from fastapi import FastAPI, Depends, Request, HTTPException, status, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from jose import JWTError
from typing import List, Optional

from .database import engine, SessionLocal
from . import models, schemas, crud, auth, email_utils

load_dotenv()

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


def get_current_user(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Autenticación requerida")

    try:
        payload = auth.decode_access_token(token)
        email = payload.get("sub")
        token_type = payload.get("type")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")

    if not email:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")

    user = crud.get_user_by_email(db, email)
    if not user or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario no encontrado")
    if not user.is_verified:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Verifica tu correo electrónico antes de continuar")

    return user


def get_current_user_optional(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")
    if not token:
        return None

    try:
        payload = auth.decode_access_token(token)
        email = payload.get("sub")
    except JWTError:
        return None

    if not email:
        return None

    return crud.get_user_by_email(db, email)


@app.get("/", response_class=HTMLResponse)
def home(request: Request, db: Session = Depends(get_db)):
    user = get_current_user_optional(request, db)
    return templates.TemplateResponse("index.html", {"request": request, "user": user})


@app.get("/register", response_class=HTMLResponse)
def register_form(request: Request):
    return templates.TemplateResponse("register.html", {"request": request, "error": None, "success": None})


@app.post("/register", response_class=HTMLResponse)
async def register(request: Request, nombre_apellido: str = Form(...), email: str = Form(...), password: str = Form(...), cargo: str = Form(...), db: Session = Depends(get_db)):
    existing = crud.get_user_by_email(db, email)
    if existing:
        return templates.TemplateResponse("register.html", {"request": request, "error": "Este correo ya está registrado.", "success": None})

    user = schemas.UserCreate(nombre_apellido=nombre_apellido, email=email, password=password, cargo=cargo)
    db_user = crud.create_user(db, user)
    token = auth.create_access_token({"sub": db_user.email, "type": "verify"}, expires_delta=timedelta(hours=24))
    await email_utils.send_verification_email(db_user.email, token)

    message = "Registro exitoso. Revisa tu correo para verificar tu cuenta."
    return templates.TemplateResponse("register.html", {"request": request, "error": None, "success": message})


@app.get("/verify", response_class=HTMLResponse)
def verify(request: Request, token: str, db: Session = Depends(get_db)):
    try:
        payload = auth.decode_access_token(token)
        email = payload.get("sub")
        token_type = payload.get("type")
    except JWTError:
        return templates.TemplateResponse("verify.html", {"request": request, "error": "Token inválido o expirado.", "message": None})

    if token_type != "verify" or not email:
        return templates.TemplateResponse("verify.html", {"request": request, "error": "Token inválido.", "message": None})

    user = crud.verify_user(db, email)
    if not user:
        return templates.TemplateResponse("verify.html", {"request": request, "error": "No se encontró el usuario.", "message": None})

    return templates.TemplateResponse("verify.html", {"request": request, "error": None, "message": "Cuenta verificada con éxito. Ya puedes iniciar sesión."})


@app.get("/login", response_class=HTMLResponse)
def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "error": None})


@app.post("/login", response_class=HTMLResponse)
def login(request: Request, email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = crud.authenticate_user(db, email, password)
    if not user:
        return templates.TemplateResponse("login.html", {"request": request, "error": "Correo o contraseña incorrectos."})
    if not user.is_verified:
        return templates.TemplateResponse("login.html", {"request": request, "error": "Verifica tu correo antes de ingresar."})

    token = auth.create_access_token({"sub": user.email, "type": "access"}, expires_delta=timedelta(hours=8))
    response = RedirectResponse(url="/admin", status_code=status.HTTP_302_FOUND)
    response.set_cookie("access_token", token, httponly=True, samesite="lax", max_age=3600 * 8)
    return response


@app.get("/logout")
def logout():
    response = RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    response.delete_cookie("access_token")
    return response


@app.post("/solicitudes", response_model=schemas.Solicitud)
async def crear_solicitud(solicitud: schemas.SolicitudCreate, db: Session = Depends(get_db)):
    nueva = crud.crear_solicitud(db, solicitud)
    await email_utils.send_status_email(solicitud.correo, solicitud.nombre_apellido, "Registrada")
    return nueva


@app.get("/solicitudes", response_model=List[schemas.Solicitud])
def listar_solicitudes(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return crud.obtener_solicitudes(db)


@app.post("/solicitud/{solicitud_id}/estado_solicitud", response_model=schemas.Solicitud)
async def actualizar_estado_solicitud(solicitud_id: int, payload: schemas.EstadoUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if not payload.estado_solicitud:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Estado de solicitud requerido")
    solicitud = crud.actualizar_estado_solicitud(db, solicitud_id, payload.estado_solicitud)
    if not solicitud:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Solicitud no encontrada")
    await email_utils.send_status_email(solicitud.correo, solicitud.nombre_apellido, solicitud.estado1)
    return solicitud


@app.post("/solicitud/{solicitud_id}/estado_maquina", response_model=schemas.Solicitud)
async def actualizar_estado_maquina(solicitud_id: int, payload: schemas.EstadoUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if not payload.estado_maquina:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Estado de máquina requerido")
    solicitud = crud.actualizar_estado_maquina(db, solicitud_id, payload.estado_maquina)
    if not solicitud:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Solicitud no encontrada")
    await email_utils.send_status_email(solicitud.correo, solicitud.nombre_apellido, solicitud.estado2)
    return solicitud


@app.post("/solicitud/{solicitud_id}/aprobar", response_model=schemas.Solicitud)
async def aprobar_solicitud(solicitud_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    solicitud = crud.aprobar_solicitud(db, solicitud_id)
    if not solicitud:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Solicitud no encontrada")
    await email_utils.send_status_email(solicitud.correo, solicitud.nombre_apellido, "Aprobada")
    return solicitud


@app.post("/solicitud/{solicitud_id}/rechazar", response_model=schemas.Solicitud)
async def rechazar_solicitud(solicitud_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    solicitud = crud.rechazar_solicitud(db, solicitud_id)
    if not solicitud:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Solicitud no encontrada")
    await email_utils.send_status_email(solicitud.correo, solicitud.nombre_apellido, "Rechazada")
    return solicitud


@app.get("/admin", response_class=HTMLResponse)
def admin(request: Request, db: Session = Depends(get_db)):
    user = get_current_user_optional(request, db)
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse("admin.html", {"request": request, "user": user})
