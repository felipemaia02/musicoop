"""
    Módulo responsavel pelos métados de querys com a tabela post
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
        Função que pega as publicações do banco de dados

      Parameters
      ----------
        database : Session
            Sessão do banco de dados
      
      Return
      ------
        Publicações
        
    """

    posts = database.query(Post).order_by(Post.id.desc()).all()
    logger.info("FOI RETORNADO DO BANCO AS SEGUINTES CONTRIBUIÇÕES: %s", posts)

    return posts

def get_post_by_name(post_name:str, database: Session) -> Post:
    """
        Description
        -----------
            Função que retorna uma publicação específica pelo nome

        Parameters
        ----------
            post_name : String
                Nome da publicação
        Return
        ------
            Publicação
    """
    post = database.query(Post).filter(Post.post_name == post_name).first()
    logger.info("FOI RETORNADO DO BANCO AS SEGUINTES CONTRIBUIÇÕES: %s", post)

    return post

def get_post_by_id(post_id:int, database: Session) -> Post:
    """
        Description
        -----------
            Função que retorna uma publicação específica pelo id

        Parameters
        ----------
            post_name : Integer
                Id da publicação
        Return
        ------
            Publicação
    """
    post = database.query(Post).filter(Post.id == post_id).first()

    logger.info("FOI RETORNADO DO BANCO AS SEGUINTES CONTRIBUIÇÕES: %s", post)

    return post

def create_post(request: PostSchema,
                   database: Session) -> Post:
    """
      Description
      -----------
        Função que cria uma publicação

      Parameters
      ----------
        request : PostSchema
            Parâmetro com a tipagem da publicação
            
      Return
      ------
        Publicação criada
    """
    new_post = Post(post_name=request.post_name,file=request.file,
                          file_size=request.file_size,user=request.user,
                          description=request.description)
    database.add(new_post)
    database.commit()
    logger.info("FOI CRIADO NO BANCO A SEGUINTE CONTRIBUIÇÃO: %s", new_post)
    return new_post

def delete_post(post_id: int, database: Session) -> Post:
    """
      Description
      -----------
        Função que deleta uma publicação

      Parameters
      ----------
        post_id : Integer
            Id da publicação
      Return
      ------
        Publicação deletada
    """

    get_post = get_post_by_id(post_id, database)

    database.delete(get_post)
    database.commit()

    return get_post
