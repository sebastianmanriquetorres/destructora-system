import os
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

mail_config = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME", ""),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD", ""),
    MAIL_FROM=os.getenv("MAIL_FROM", "no-reply@example.com"),
    MAIL_PORT=int(os.getenv("MAIL_PORT", "587")),
    MAIL_SERVER=os.getenv("MAIL_SERVER", "smtp.gmail.com"),
    MAIL_STARTTLS=bool(os.getenv("MAIL_TLS", "True") == "True"),
    MAIL_SSL_TLS=bool(os.getenv("MAIL_SSL", "False") == "True"),
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)


async def send_email(subject: str, email_to: str, body: str) -> None:
    message = MessageSchema(
        subject=subject,
        recipients=[email_to],
        body=body,
        subtype="html"
    )
    fast_mail = FastMail(mail_config)
    await fast_mail.send_message(message)


async def send_verification_email(email_to: str, token: str) -> None:
    url = os.getenv("BASE_URL", "http://localhost:8000")
    verify_link = f"{url}/verify?token={token}"
    body = f"<p>Hola,</p>" \
           f"<p>Gracias por registrarte. Haz clic en el siguiente enlace para verificar tu correo electrónico:</p>" \
           f"<p><a href=\"{verify_link}\">Verificar cuenta</a></p>" \
           f"<p>Si no solicitaste este correo, ignora este mensaje.</p>"
    await send_email("Verifica tu cuenta", email_to, body)


async def send_status_email(email_to: str, nombre: str, estado: str) -> None:
    body = f"<p>Hola {nombre},</p>" \
           f"<p>Tu solicitud de la máquina destructora de papel ha cambiado de estado a: <strong>{estado}</strong>.</p>" \
           f"<p>Si necesitas más información, responde a este correo o contacta al equipo de soporte.</p>"
    await send_email("Actualización de estado de solicitud", email_to, body)
