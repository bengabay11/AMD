import imghdr
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.errors import MessageError
import os

from src.server import config

SMTP_SERVER_HOST = 'smtp.gmail.com'
SMTP_SERVER_PORT = 587


class EmailSender:
    def __init__(self, from_address, password):
        self.from_address = from_address
        self.server = smtplib.SMTP(SMTP_SERVER_HOST, SMTP_SERVER_PORT)
        self.server.starttls()
        self.server.login(self.from_address, password)

    def create_message(self, to, body, subject=None):
        msg = MIMEMultipart()
        msg['From'] = self.from_address
        msg['To'] = to
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        return msg

    def send_new_email(self, message):
        try:
            self.server.sendmail(self.from_address, message['To'], message.as_string())
            return "Success"
        except MessageError:
            return "Fail"

    @staticmethod
    def attach_file(msg, file_path):
        if os.path.exists(file_path):
            attachment_file = open(file_path, config.FILE_READ_MODE)
            image_data = attachment_file.read()
            msg.add_attachment(image_data, maintype='image', subtype=imghdr.what(None, image_data))

