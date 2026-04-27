import sys
sys.path.insert(0, '.')
import asyncio
from app import email_utils

async def test_email():
    try:
        print("Probando envío de email...")
        await email_utils.send_verification_email("sebastian.manrique.torres@gmail.com", "test_token_123")
        print("Email enviado exitosamente")
    except Exception as e:
        print(f"Error enviando email: {e}")
        import traceback
        traceback.print_exc()

# Ejecutar la función asíncrona
asyncio.run(test_email())