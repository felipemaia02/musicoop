"""
Model responsável por salvar usuários da aplicação
"""
from sqlalchemy import Column, Integer,String, ForeignKey, Time, Boolean, LargeBinary

from musicoop.database import Base

class Contribuition(Base):
    """
      Classe responsável pela tabela contribuition

      Attributes
        ----------
            name          : str
                Nome dá contribuição
            aproved       : boolean
                Aprovação dá contribuição
            file          : blob
                Arquivo dá Contribuição
            music         : int
                Nome dá Contribuição
            user          : int
                ID do usuário que criou a Contribuição
            creation_date : time
                Data de criação
    """
    __tablename__="contribuition"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    aproved = Column(Boolean, nullable=False)
    file = Column(LargeBinary, nullable=False)
    music = Column(Integer, ForeignKey('music.id'))
    user = Column(Integer, ForeignKey('user.id'))
    creation_date = Column(Time, nullable=False)
