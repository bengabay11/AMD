import imghdr
import smtplib
from email.errors import MessageError
import os
from email.message import EmailMessage


SMTP_SERVER_HOST = 'smtp.gmail.com'
SMTP_SERVER_PORT = 587


class Email:
    """The class connects to a gmail account and send messages"""
    def __init__(self, from_adrr, password):
            self.from_adrr = from_adrr
            self.password = password
            self.file_name = ''
            self.subject = ''
            self.body = ''
            self.to = ''
            self.msg = ''

    def send_new_email(self, to, body, subject=None, file_name=''):
        """The function gets the new email details, connect to the account with the from_adrr and password, and send
         the email."""
        self.subject = subject
        self.body = body
        self.file_name = file_name
        self.to = to

        self.msg = EmailMessage()
        self.msg['From'] = self.from_adrr
        self.msg['To'] = self.to

        self.msg.set_content(self.body, 'plain')
        try:
            self.add_file_to_message()
        finally:
            pass
        try:
            self.msg['Subject'] = self.subject
        finally:
            pass
        try:
            server = smtplib.SMTP(SMTP_SERVER_HOST, SMTP_SERVER_PORT)
            server.starttls()
            server.login(self.from_adrr, self.password)
            text = self.msg.as_string()
            server.sendmail(self.from_adrr, self.to, text)
            server.quit()
            return "Success"
        except MessageError:
            return "Fail"

    def add_file_to_message(self):
        # The function attach file to the message
        if os.path.exists(self.file_name):
            attachment_file = open(self.file_name, "rb")
            image_data = attachment_file.read()
            self.msg.add_attachment(image_data, maintype='image', subtype=imghdr.what(None, image_data))
