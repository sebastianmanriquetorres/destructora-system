import sys
sys.path.insert(0, '.')
from app.database import SessionLocal
from app import models

db = SessionLocal()
users = db.query(models.User).all()
print(f"Total usuarios: {len(users)}")
for user in users:
    print(f"- {user.email}: {user.nombre_apellido} (verificado: {user.is_verified}, activo: {user.is_active})")
db.close()