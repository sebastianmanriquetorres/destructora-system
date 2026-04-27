import sys
sys.path.insert(0, '.')

password = "123"
print(f"Password: '{password}'")
print(f"Length: {len(password)}")
print(f"Bytes: {len(password.encode('utf-8'))}")

from app import auth
print("Intentando hashear...")
try:
    hashed = auth.get_password_hash(password)
    print(f"Hash exitoso: {hashed}")
except Exception as e:
    print(f"Error en hash: {e}")
    import traceback
    traceback.print_exc()