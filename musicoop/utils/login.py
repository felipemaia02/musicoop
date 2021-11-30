'''
Modulo de criação do token no login
'''
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from jose import jwt

from musicoop.settings.logs import logging

logger = logging.getLogger(__name__)
load_dotenv()

def create_access_token(data: dict) -> str:
    """Função utilizada para criar o token de acesso após login do usuário

    Parameters
    ----------
      data : dict
          Dados do usuário que serão salvos no token.

    Returns
    -------
      Dicionário com o token de acesso e data de expiração do token.
    """

    expire_date = datetime.utcnow() + timedelta(hours=int(os.getenv('ACCESS_TOKEN_EXPIRE_HOURS')))
    data.update({"expire_token": str(expire_date)})
    refresh_token = jwt.encode(data, os.getenv('SECRET_KEY'), algorithm="HS256")
    logger.info("ACCESS TOKEN GERADO COM SUCESSO")
    return refresh_token


def generate_password() -> str:
    """
    """