import smtplib
from email.message import EmailMessage

from app.auth.application.ports.password_reset_notifier import IPasswordResetNotifier


class SmtpPasswordResetNotifier(IPasswordResetNotifier):
    def __init__(self, host: str, port: int, sender: str) -> None:
        self._host = host
        self._port = port
        self._sender = sender

    def send(self, email: str, token: str) -> None:
        message = EmailMessage()
        message["Subject"] = "LifeOS password reset"
        message["From"] = self._sender
        message["To"] = email
        message.set_content(
            "Use this token to reset your LifeOS password: "
            + token
        )
        with smtplib.SMTP(self._host, self._port, timeout=10) as smtp:
            smtp.send_message(message)
