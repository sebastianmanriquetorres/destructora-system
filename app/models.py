from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    nombre_apellido = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    cargo = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Solicitud(Base):
    __tablename__ = "solicitudes"

    id = Column(Integer, primary_key=True, index=True)
    nombre_apellido = Column(String)
    cedula = Column(String)
    correo = Column(String)
    cargo = Column(String)
    proceso = Column(String)
    fecha_inicio = Column(String)
    hora_inicio = Column(String)
    fecha_fin = Column(String)
    hora_fin = Column(String)
    estado1 = Column(String, default="Pendiente")
    estado2 = Column(String, default="Disponible")