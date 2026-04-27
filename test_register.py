import sys
sys.path.insert(0, '.')
print("Importando modulos...")
from app.database import SessionLocal
print("BD importado")
from app import crud
print("CRUD importado")
from app.schemas import UserCreate
print("Schemas importado")

print("Probando registro...")
db = SessionLocal()
try:
    user_data = UserCreate(
        nombre_apellido="Test Admin",
        email="test@example.com",
        password="123",
        cargo="Test"
    )
    db_user = crud.create_user(db, user_data)
    print("Usuario creado exitosamente")
    db.commit()
except Exception as e:
    print(f"Error: {e}")
    db.rollback()
finally:
    db.close()