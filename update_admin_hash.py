import sys
sys.path.insert(0, '.')
from app.database import SessionLocal
from app import models, auth

db = SessionLocal()
try:
    # Buscar usuario admin
    admin = db.query(models.User).filter(models.User.email == "admin@example.com").first()
    if admin:
        # Actualizar hash de contraseña
        admin.hashed_password = auth.get_password_hash("123")
        db.commit()
        print("Hash de contraseña del admin actualizado")
    else:
        print("Admin no encontrado")
except Exception as e:
    print(f"Error: {e}")
    db.rollback()
finally:
    db.close()