from sqlalchemy.orm import Session
from . import models, schemas

def crear_solicitud(db: Session, solicitud: schemas.SolicitudCreate):

    nueva = models.Solicitud(
        nombre_apellido=solicitud.nombre_apellido,
        cedula=solicitud.cedula,
        correo=solicitud.correo,
        cargo=solicitud.cargo,
        proceso=solicitud.proceso,
        fecha_inicio=solicitud.fecha_inicio,
        hora_inicio=solicitud.hora_inicio,
        fecha_fin=solicitud.fecha_fin,
        hora_fin=solicitud.hora_fin
    )

    db.add(nueva)
    db.commit()
    db.refresh(nueva)

    return nueva


def obtener_solicitudes(db: Session):
    return db.query(models.Solicitud).all()