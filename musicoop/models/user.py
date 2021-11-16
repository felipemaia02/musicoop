"""
Model responsável por salvar usuários da aplicação
"""
from datetime import datetime
from sqlalchemy import Column, Integer,String, DateTime
from sqlalchemy.orm import relationship

from musicoop.database import Base
from musicoop.models.comment import Comment
from musicoop.models.contribuition import Contribuition
from musicoop.models.post import Post
from musicoop.models.vote import Vote


class User(Base):
    """
      Classe responsável pela tabela user

      Attributes
        ----------
            id : int
                id do usuário
            email : str
                Email do usuário
            name : str
                Nome do usuário
            username : str
                Username do usuário
            password : str
                Senha do usuário
            access_token : str
                Token de sessão do usuário
            creation_date : time
                Data de criação
    """
    __tablename__="user"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    access_token = Column(String)
    creation_date = Column(DateTime, default=datetime.now(),nullable=False)

    comment = relationship(Comment)
    contribuition = relationship(Contribuition)
    post = relationship(Post)
    vote = relationship(Vote)

    def __init__(self, email=None, name=None, username=None, password=None):
        self.email = email
        self.name = name
        self.username = username
        self.password = password
