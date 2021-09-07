"""
Model responsável por salvar usuários da aplicação
"""
from sqlalchemy import Column, Integer,String, ForeignKey, Time

from musicoop.database import Base


class Comment(Base):
    """
      Classe responsável pela tabela comments

      Attributes
        ----------
            music         : str
                Nome dá música
            comment       : str
                Comentário dá música
            user          : int
                ID do usuário que criou o comentário
            creation_date : time
                Data de criação
    """
    __tablename__="comments"
    id = Column(Integer, primary_key=True, index=True)
    music = Column(Integer, ForeignKey('music.id'))
    comment = Column(String, nullable=False)
    user = Column(Integer, ForeignKey('user.id'))
    creation_date = Column(Time, nullable=False)
