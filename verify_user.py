import sys
sys.path.insert(0, '.')
from app.database import SessionLocal
from app import models

db = SessionLocal()
user = db.query(models.User).filter(models.User.email == "sebastian.manrique.torres@gmail.com").first()
if user:
    user.is_verified = True
    db.commit()
    print(f"Usuario {user.email} verificado exitosamente")
else:
    print("Usuario no encontrado")
db.close()