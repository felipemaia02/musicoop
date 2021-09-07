"""
Model responsável por salvar usuários da aplicação
"""
from sqlalchemy import Column, Integer,String, ForeignKey, Time, BLOB

from musicoop.database import Base


class Music(Base):
    """
      Classe responsável pela tabela music

      Attributes
        ----------
            music_name    : str
                Nome dá música
            file          : str
                Arquivo dá música
            user          : int
                ID do usuário que criou a música
            creation_date : time
                Data de criação
    """
    __tablename__="music"
    id = Column(Integer, primary_key=True, index=True)
    music_name = Column(String, nullable=False)
    file = Column(BLOB, nullable=False)
    user = Column(Integer, ForeignKey('user.id'))
    creation_date = Column(Time, nullable=False)
