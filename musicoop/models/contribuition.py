"""
Model responsável por salvar contribuições da aplicação
"""
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from datetime import datetime
from musicoop.database import Base


class Contribuition(Base):
    """
      Classe responsável pela tabela contribuition

      Attributes
        ----------
            id : int
                Id da contribuição
            name : str
                Nome da contribuição
            aproved : boolean
                Aprovação da contribuição
            file : str
                Arquivo da Contribuição
            file_size : int
                Tamanho do Arquivo de Contribuição
            description : str
                Descrição da contribuição
            post : int
                Id da publicação a qual a Contribuição está atrelada
            user : int
                ID do usuário que criou a Contribuição
            creation_date : time
                Data de criação
    """
    __tablename__ = "contribuition"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    aproved = Column(Boolean, default=False, nullable=False)
    file = Column(String, nullable=True)
    file_size = Column(Integer, nullable=True)
    description = Column(String, nullable=False)
    post = Column(Integer, ForeignKey('post.id'))
    user = Column(Integer, ForeignKey('user.id'))
    username = Column(String, nullable=False)
    creation_date = Column(DateTime, default=datetime.now(), nullable=False)

    def __init__(self, name=None, file=None, file_size=None, user=None, post=None, description=None, username=None):
        self.name = name
        self.file = file
        self.user = user
        self.description = description
        self.post = post
        self.file_size = file_size
        self.username = username
