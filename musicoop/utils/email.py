"""
Modulo
"""
import os
import smtplib
import re
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

from .login import generate_password
from musicoop.settings.logs import logging

logger = logging.getLogger(__name__)
load_dotenv()


class SendEmail():

    def validate_email(self, email: str) -> bool:
        """
        """
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

        if(re.fullmatch(regex, email)):
            return True

        else:
            return False

    def welcome_email(self, reciver_address, name) -> bool:
        """
        """
        content = f"""
                    Seja bem-vindo {name} ao Musicoop!

                    Esse email é apenas de confirmação que sua conta foi criada com sucesso!

                    Obrigado,
                    Equipe Musicoop!
                    """
        email = self.send_email(
            content, reciver_address, "Cadastro concluido!")
        if email is False:
            return False
        return True

    def reset_password_email(self) -> None:
        """
        """
        pass

    def change_password_email(self) -> None:
        """
        """
        pass

    def send_email(self,
                   content: str,
                   reciver_adress: str,
                   suject: str) -> bool:
        """
        """
        try:
            message = MIMEMultipart()
            message['From'] = os.getenv('MUSICOOP_EMAIL')
            message['To'] = reciver_adress
            message['Subject'] = suject
            message.attach(MIMEText(content, 'plain'))
            session = smtplib.SMTP('smtp.gmail.com', 587)
            session.starttls()
            session.login(os.getenv('MUSICOOP_EMAIL'),
                          os.getenv('MUSICOOP_EMAIL_PASSWORD'))
            text = message.as_string()
            session.sendmail(os.getenv('MUSICOOP_EMAIL'),
                             reciver_adress, text)
            logger.info("EMAIL ENVIADO COM SUCESSO")
        except smtplib.SMTPRecipientsRefused as err:
            logger.info("NÃO FOI POSSIVEL ENVIAR O EMAIL", err)
            pass

        finally:
            logger.info("FECHANDO A SESSÃO")
            session.quit()
