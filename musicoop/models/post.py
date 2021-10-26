"""
Model responsável por salvar usuários da aplicação
"""
from datetime import datetime
from sqlalchemy import Column, Integer,String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from musicoop.database import Base


class Post(Base):
    """
      Classe responsável pela tabela post

      Attributes
        ----------
            post_name  : str
                Nome dá música
            path          : str
                Caminho da música
            file          : str
                Arquivo da música
            user          : int
                ID do usuário que criou a música
            creation_date : time
                Data de criação
    """
    __tablename__="post"
    id = Column(Integer, primary_key=True, index=True)
    post_name = Column(String, nullable=False)
    file = Column(String, nullable=False)
    file_size = Column(Integer, nullable=False)
    description = Column(String, nullable=False)
    user = Column(Integer, ForeignKey('user.id'))
    creation_date = Column(DateTime, default=datetime.now(),nullable=False)

    comment_relation = relationship("Comment", back_populates="post_relation")

    def __init__(self, post_name=None,file=None,file_size=None,user=None,description=None):
        self.post_name = post_name
        self.file = file
        self.description = description
        self.user = user
        self.file_size = file_size
