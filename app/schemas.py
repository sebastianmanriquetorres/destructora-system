from typing import Optional
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    nombre_apellido: str
    email: EmailStr
    password: str
    cargo: str


class UserRead(BaseModel):
    id: int
    nombre_apellido: str
    email: EmailStr
    cargo: Optional[str]
    is_verified: bool

    class Config:
        from_attributes = True


class SolicitudCreate(BaseModel):
    nombre_apellido: str
    correo: EmailStr
    cedula: str
    cargo: str
    proceso: str
    fecha_inicio: str
    hora_inicio: str
    fecha_fin: str
    hora_fin: str


class EstadoUpdate(BaseModel):
    estado_solicitud: Optional[str] = None
    estado_maquina: Optional[str] = None


class Solicitud(BaseModel):
    id: int
    nombre_apellido: str
    cedula: str
    correo: str
    cargo: str
    proceso: str
    fecha_inicio: str
    hora_inicio: str
    fecha_fin: str
    hora_fin: str
    estado1: str
    estado2: str

    class Config:
        from_attributes = True
