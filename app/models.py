from sqlalchemy import Column, Integer, String
from .database import Base

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

    estado1 = Column(String, default="Prestada")
    estado2 = Column(String, default="En préstamo")