"""
Model responsável por salvar usuários da aplicação
"""
from datetime import datetime
from sqlalchemy import Column, Integer,String, ForeignKey, DateTime, LargeBinary

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
    file = Column(LargeBinary, nullable=False)
    user = Column(Integer, ForeignKey('user.id'))
    creation_date = Column(DateTime, default=datetime.now(),nullable=False)

    def __init__(self, music_name=None,file=None,user=None):
        self.music_name = music_name
        self.file = file
        self.user = user
