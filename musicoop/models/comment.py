"""
Model responsável por salvar comentários da aplicação
"""
from datetime import datetime
from sqlalchemy import Column, Integer,String, ForeignKey, DateTime
from sqlalchemy.orm import relationship


from musicoop.database import Base


class Comment(Base):
    """
      Classe responsável pela tabela comments

      Attributes
      ----------
            music : str
                Nome dá música
            comment : str
                Comentário dá música
            pos : int
                Id da publiação ao qual será atrelado o comentário
            user : int
                ID do usuário que criou o comentário
            creation_date : time
                Data de criação
    """
    __tablename__="comment"
    id = Column(Integer, primary_key=True, index=True)
    comment = Column(String, nullable=False)
    post = Column(Integer, ForeignKey('post.id'), nullable=False)
    user = Column(Integer, ForeignKey('user.id'), nullable=False)
    creation_date = Column(DateTime, default=datetime.now(),nullable=False)

    post_relation = relationship("Post", back_populates="comment_relation")

    def __init__(self, post=None, comment=None, user=None):
        self.post = post
        self.comment = comment
        self.user = user
