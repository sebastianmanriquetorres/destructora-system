import sys
sys.path.insert(0, '.')
from app.database import SessionLocal
from app import models, crud, auth
from app.schemas import UserCreate

db = SessionLocal()
try:
    admin_data = UserCreate(
        nombre_apellido="Administrador",
        email="admin@example.com",
        password="123",
        cargo="Administrador"
    )
    admin = crud.create_user(db, admin_data)
    admin.is_verified = True
    admin.is_active = True
    db.commit()
    print("Usuario admin creado: admin@example.com / 123")
except Exception as e:
    print(f"Error: {e}")
finally:
    db.close()