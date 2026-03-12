from sqlalchemy import Column, Integer, String
from .database import Base


class Solicitud(Base):
    __tablename__ = "solicitudes"

    id = Column(Integer, primary_key=True, index=True)
    solicitante = Column(String)
    correo = Column(String)
    dependencia = Column(String)
    fecha_inicio = Column(String)
    fecha_fin = Column(String)
    motivo = Column(String)
    estado = Column(String, default="pendiente")