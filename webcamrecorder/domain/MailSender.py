import ssl
from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate
from . import Frame

class MailSender:
    can_send = True
    def __init__(self, host: str, port: str, account: str, password: str) -> None:
        if host == "" or port == "" or account == "" or password == "":
            self.can_send = False
        self.host = host
        self.port = port
        self.account = account
        self.password = password

    def send(self, frame: Frame.Frame, subect: str = "subject", body: str = "body"):
        if self.can_send == False:
            return

        msg = MIMEMultipart()
        msg["Subject"] = subect
        msg["From"] = self.account
        msg["To"] = self.account
        msg["Date"] = formatdate()

        msg.attach(MIMEText(body, "plain", "utf-8"))

        msg.attach(MIMEImage(frame.encode()))

        context = ssl.create_default_context()
        server = SMTP_SSL(self.host, self.port, context=context)

        server.login(self.account, self.password)

        server.send_message(msg)

        server.quit()
