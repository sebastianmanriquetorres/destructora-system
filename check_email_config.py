import os
from dotenv import load_dotenv

load_dotenv()

print("CONFIGURACION DE EMAIL:")
print("MAIL_USERNAME:", os.getenv('MAIL_USERNAME', 'NO CONFIGURADO'))
print("MAIL_SERVER:", os.getenv('MAIL_SERVER', 'NO CONFIGURADO'))
print("MAIL_PORT:", os.getenv('MAIL_PORT', 'NO CONFIGURADO'))

username = os.getenv('MAIL_USERNAME', '')
password = os.getenv('MAIL_PASSWORD', '')

if username and password and username != 'tu_correo@gmail.com':
    print("CONFIGURACION COMPLETA - Los emails deberian funcionar")
else:
    print("CONFIGURACION INCOMPLETA - Configura tus credenciales en .env")