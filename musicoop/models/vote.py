"""
Model responsável por salvar votos das contribuições da publicação da aplicação
"""
from sqlalchemy import Column, Integer, ForeignKey, Time

from musicoop.database import Base


class Vote(Base):
    """
      Classe responsável pela tabela vote

      Attributes
        ----------
            post : int
                ID da publicação
            contribuition : int
                ID da contribuição da publicação
            user : int
                ID do usuário que fez o voto
            creation_date : time
                Data de criação
    """
    __tablename__="vote"
    id = Column(Integer, primary_key=True, index=True)
    post = Column(Integer, ForeignKey('post.id'))
    contribuition = Column(Integer, ForeignKey('contribuition.id'))
    user = Column(Integer, ForeignKey('user.id'))
    creation_date = Column(Time, nullable=False)
