import sys
sys.path.insert(0, '.')
from app.database import SessionLocal
from app import models

db = SessionLocal()
admin = db.query(models.User).filter(models.User.email == "admin@example.com").first()
print(f"Admin encontrado: {admin is not None}")
if admin:
    print(f"Email: {admin.email}")
    print(f"Verificado: {admin.is_verified}")
    print(f"Activo: {admin.is_active}")
db.close()