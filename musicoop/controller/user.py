"""
    Módulo responsavel pelos métados de querys com a tabela usuário
"""

import hashlib
from sqlalchemy.orm import Session

from musicoop.schemas.user import CreateUserSchema, UserSchema
from musicoop.models.user import User
from musicoop.settings.logs import logging

logger = logging.getLogger(__name__)


def get_user(email: str, database: Session) -> User:
    """
      Description
      -----------
        Função que pega um usuário específico a partir do email

      Parameters
      ----------
        email : String
          Email do usuário
      
      Return
      ------
        Usuário

    """

    user = database.query(User).filter(User.email == email).first()
    logger.info("FOI RETORNADO DO BANCO O SEGUINTE EMAIL: %s", email)

    return user


def get_user_by_id(id: str, database: Session) -> User:
    """
      Description
      -----------
        Função que pega um usuário específico a partir do id

      Parameters
      ----------
        id : Integer
          Id do usuário
      
      Return
      ------
        Usuário

    """

    user = database.query(User).filter(User.id == id).first()
    logger.info("FOI RETORNADO DO BANCO O SEGUINTE EMAIL: %s", user)

    return user


def create_user(request: CreateUserSchema, database: Session) -> User:
    """
      Description
      -----------
        Função que cria um usuário

      Parameters
      ----------
        request : CreatUserSchema
          Parâmetro com a tipagem dos dados do usuário
      
      Return
      ------
        Usuário criado

    """
    password = hashlib.sha256(request.password.encode()).hexdigest()

    new_user = User(email=request.email, name=request.name,
                    username=request.username, password=password)
    database.add(new_user)
    database.commit()
    logger.info("FOI CRIADO NO BANCO O SEGUINTE USUÁRIO: %s", new_user)
    return new_user
