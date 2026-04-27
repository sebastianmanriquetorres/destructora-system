from sqlalchemy.orm import Session
from . import models, schemas, auth


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(
        nombre_apellido=user.nombre_apellido,
        email=user.email,
        hashed_password=hashed_password,
        cargo=user.cargo
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not auth.verify_password(password, user.hashed_password):
        return None
    return user


def verify_user(db: Session, email: str):
    user = get_user_by_email(db, email)
    if not user:
        return None
    user.is_verified = True
    db.commit()
    db.refresh(user)
    return user


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
    return db.query(models.Solicitud).order_by(models.Solicitud.id.desc()).all()


def obtener_solicitud(db: Session, solicitud_id: int):
    return db.query(models.Solicitud).filter(models.Solicitud.id == solicitud_id).first()


def actualizar_estado_solicitud(db: Session, solicitud_id: int, nuevo_estado: str):
    solicitud = obtener_solicitud(db, solicitud_id)
    if not solicitud:
        return None

    solicitud.estado1 = nuevo_estado
    db.commit()
    db.refresh(solicitud)
    return solicitud


def actualizar_estado_maquina(db: Session, solicitud_id: int, nuevo_estado: str):
    solicitud = obtener_solicitud(db, solicitud_id)
    if not solicitud:
        return None

    solicitud.estado2 = nuevo_estado
    db.commit()
    db.refresh(solicitud)
    return solicitud


def aprobar_solicitud(db: Session, solicitud_id: int):
    solicitud = obtener_solicitud(db, solicitud_id)
    if not solicitud:
        return None

    solicitud.estado1 = "Aprobada"
    solicitud.estado2 = "Prestada"
    db.commit()
    db.refresh(solicitud)
    return solicitud


def rechazar_solicitud(db: Session, solicitud_id: int):
    solicitud = obtener_solicitud(db, solicitud_id)
    if not solicitud:
        return None

    solicitud.estado1 = "Rechazada"
    solicitud.estado2 = "Disponible"
    db.commit()
    db.refresh(solicitud)
    return solicitud
