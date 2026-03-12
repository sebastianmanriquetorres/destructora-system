from pydantic import BaseModel


class SolicitudCreate(BaseModel):
    solicitante: str
    correo: str
    dependencia: str
    fecha_inicio: str
    fecha_fin: str
    motivo: str


class Solicitud(SolicitudCreate):
    id: int
    estado: str

    class Config:
        from_attributes = True