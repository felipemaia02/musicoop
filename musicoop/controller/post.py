"""
    Módulo responsavel pelos métados de querys com a tabela usuário
"""
from typing import List
from sqlalchemy.orm import Session
from musicoop.schemas.post import PostSchema
from musicoop.models.post import Post
from musicoop.settings.logs import logging

logger = logging.getLogger(__name__)

def get_posts(database: Session) -> List:
    """
      Description
      -----------

      Parameters
      ----------
    """

    posts = database.query(Post).order_by(Post.id.desc()).all()
    logger.info("FOI RETORNADO DO BANCO AS SEGUINTES CONTRIBUIÇÕES: %s", posts)

    return posts

def get_post_by_name(post_name:str, database: Session) -> Post:
    """
        Description
        -----------

        Parameters
        ----------
    """
    post = database.query(Post).filter(Post.post_name == post_name).first()
    logger.info("FOI RETORNADO DO BANCO AS SEGUINTES CONTRIBUIÇÕES: %s", post)

    return post

def get_post_by_id(post_id:str, database: Session) -> Post:
    """
        Description
        -----------

        Parameters
        ----------
    """
    post = database.query(Post).filter(Post.id == post_id).first()

    logger.info("FOI RETORNADO DO BANCO AS SEGUINTES CONTRIBUIÇÕES: %s", post)

    return post

def create_post(request: PostSchema,
                   database: Session) -> Post:
    """
      Description
      -----------

      Parameters
      ----------
    """
    new_post = Post(post_name=request.post_name,file=request.file,
                          file_size=request.file_size,user=request.user)
    database.add(new_post)
    database.commit()
    logger.info("FOI CRIADO NO BANCO A SEGUINTE CONTRIBUIÇÃO: %s", new_post)
    return new_post

def delete_post(post_id: int, database: Session) -> Post:
    """
      Description
      -----------

      Parameters
      ----------
    """

    get_post = get_post_by_id(post_id, database)

    database.delete(get_post)
    database.commit()

    return get_post
