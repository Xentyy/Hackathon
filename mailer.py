import os, ssl, smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()


class EmailSender:
    """Basit SMTP (Gmail) gönderici."""

    def __init__(self):
        self.user = os.getenv("MAIL_USER")
        self.password = os.getenv("MAIL_PASS")
        if not (self.user and self.password):
            raise RuntimeError("MAIL_USER / MAIL_PASS .env'de tanımlı değil.")
        self.smtp = "smtp.gmail.com"
        self.port = 465
        self.context = ssl.create_default_context()

    def send(self, to_list: list[str], subject: str, body: str):
        msg = EmailMessage()
        msg["From"] = self.user
        msg["Subject"] = subject
        msg.set_content(body)

        with smtplib.SMTP_SSL(self.smtp, self.port, context=self.context) as srv:
            srv.login(self.user, self.password)
            for mail in to_list:
                msg["To"] = mail
                srv.send_message(msg)
                del msg["To"]  # sonraki alıcı için temizle
