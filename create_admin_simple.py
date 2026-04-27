import sys
sys.path.insert(0, '.')
from app.database import SessionLocal
from app import models

db = SessionLocal()
try:
    # Crear usuario admin directamente con hash precalculado
    admin = models.User(
        nombre_apellido="Administrador",
        email="admin@example.com",
        hashed_password="$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewfBPj6I3Kj9F6e",  # hash de "123"
        cargo="Administrador",
        is_verified=True,
        is_active=True
    )
    db.add(admin)
    db.commit()
    print("Usuario admin creado: admin@example.com / 123")
except Exception as e:
    print(f"Error: {e}")
finally:
    db.close()