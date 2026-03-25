from pydantic import BaseModel

class SolicitudCreate(BaseModel):
    nombre_apellido: str
    cedula: str
    correo: str
    cargo: str
    proceso: str
    fecha_inicio: str
    hora_inicio: str
    fecha_fin: str
    hora_fin: str


class Solicitud(SolicitudCreate):
    id: int
    estado1: str
    estado2: str

    class Config:
        from_attributes = True