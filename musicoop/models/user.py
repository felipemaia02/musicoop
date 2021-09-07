"""
Model responsável por salvar usuários da aplicação
"""
from sqlalchemy import Column, Integer,String, Time
from sqlalchemy_utils import EmailType
from musicoop.database import Base


class User(Base):
    """
      Classe responsável pela tabela user

      Attributes
        ----------
            email         : str
                Email do usuário
            name          : str
                Nome do usuário
            username      : str
                Username do usuário
            session_token : str
                Token de sessão do usuário
            creation_date : time
                Data de criação
    """
    __tablename__="user"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(EmailType, unique=True, nullable=False)
    name = Column(String, nullable=False)
    username = Column(String, unique=True, nullable=False)
    access_token = Column(String)
    creation_date = Column(Time, nullable=False)
