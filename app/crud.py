from sqlalchemy.orm import Session
from . import models, schemas


def crear_solicitud(db: Session, solicitud: schemas.SolicitudCreate):

    nueva = models.Solicitud(
        solicitante=solicitud.solicitante,
        correo=solicitud.correo,
        dependencia=solicitud.dependencia,
        fecha_inicio=solicitud.fecha_inicio,
        fecha_fin=solicitud.fecha_fin,
        motivo=solicitud.motivo
    )

    db.add(nueva)
    db.commit()
    db.refresh(nueva)

    return nueva


def obtener_solicitudes(db: Session):
    return db.query(models.Solicitud).all()