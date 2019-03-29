import imghdr
import smtplib
from email.errors import MessageError
import os
from email.message import EmailMessage


SMTP_SERVER_HOST = 'smtp.gmail.com'
SMTP_SERVER_PORT = 587


class Email:
    def __init__(self, from_address, password):
        self.from_address = from_address
        self.server = smtplib.SMTP(SMTP_SERVER_HOST, SMTP_SERVER_PORT)
        self.server.starttls()
        self.server.login(self.from_address, password)

    def create_message(self, to, body, subject=None):
        msg = EmailMessage()
        msg['From'] = self.from_address
        msg['To'] = to
        msg.set_content(body, 'plain')
        msg['Subject'] = subject

        return msg.as_string()

    def send_new_email(self, message):
        try:
            self.server.sendmail(self.from_address, message)
            return "Success"
        except MessageError:
            return "Fail"

    def attach_file(self, msg, file_path):
        if os.path.exists(file_path):
            attachment_file = open(file_path, "rb")
            image_data = attachment_file.read()
            msg.add_attachment(image_data, maintype='image', subtype=imghdr.what(None, image_data))

