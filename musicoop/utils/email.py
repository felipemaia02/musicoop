"""
Modulo
"""
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

from login import generate_password
from musicoop.settings.logs import logging

logger = logging.getLogger(__name__)
load_dotenv()


class SendEmail():
    def __init__(self, reciver_address) -> None:
        self.reciver_address = reciver_address

    def welcome_email(self) -> None:
        """
        """

    def reset_password_email(self) -> None:
        """
        """

    def change_password_email(self) -> None:
        """
        """

    def send_email(self, 
                   content: str, 
                   reciver_email: str, 
                   suject: str ) -> bool:
        """
        """
        message = MIMEMultipart()
        message['From'] = os.getenv('MUSICOOP_EMAIL')
        message['To'] = reciver_email
        message['Subject'] = suject
        message.attach(MIMEText(content, 'plain'))
        session = smtplib.SMTP('smtp.gmail.com', 587)
        session.starttls()
        session.login(os.getenv('MUSICOOP_EMAIL'), os.getenv('MUSICOOP_EMAIL_PASSWORD'))
        text = message.as_string()
        session.sendmail(os.getenv('MUSICOOP_EMAIL'), reciver_email, text)
        session.quit()

        return True
