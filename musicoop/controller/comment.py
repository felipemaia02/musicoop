"""
    Módulo responsavel pelos métados de querys com a tabela comments
"""
from typing import List

from sqlalchemy.orm import Session
from musicoop.schemas.comment import CommentSchema, CommentUpdateSchema
from musicoop.models.comment import Comment
# from musicoop.schemas.user import GetUserSchema
from musicoop.settings.logs import logging

logger = logging.getLogger(__name__)

def get_comment_by_post(post_id: int, database: Session) -> List:
    """
        Description
        -----------
            Função que pega comentários deum post específico

        Parameters
        ----------
            post_id : Integer

        Return
        ------
            Lista de comentários
    """
    comment = database.query(Comment).filter(Comment.post == post_id).all()
    logger.info("FOI RETORNADO DO BANCO AS SEGUINTES COMENTÁRIOS: %s", comment)

    return comment

def get_comment_by_id(comment_id: int,database: Session) -> Comment:
    """
        Description
        -----------
            Função que pega um comntário específico
            
        Parameters
        ----------
            comment_id : Integer
                id do comentário
                
        Return
        ------
            Comentário
        
    """
    comment = database.query(Comment).filter(Comment.id == comment_id).first()
    logger.info("FOI RETORNADO DO BANCO AS SEGUINTES COMENTÁRIOS: %s", comment)

    return comment

def create_comment(request: CommentSchema, current_user: int, database: Session) -> Comment:
    """
        Description
        -----------
            Função que cria um comentário
            
        Parameters
        ----------
            request : CommentSchema
                Parâmetro com a tipagem do schema dos comentários
            current_user : Integer
                id do usuário logado
        
        Return
        ------
            Comentário criado

    """

    new_comment = Comment(user=current_user, post=request.post, comment=request.comment)
    database.add(new_comment)
    database.commit()
    logger.info("FOI CRIADO NO BANCO A SEGUINTE CONTRIBUIÇÃO: %s", new_comment)
    return new_comment

def delete_comment(comment_id: int,database: Session) -> Comment:
    """
        Description
        -----------
            Função que deleta um comentário
            
        Parameters
        ----------
            comment_id : Integer
                id do comentário
        
        Return
        ------
            Comentário deletado

    """

    get_comment = get_comment_by_id(comment_id, database)
    database.delete(get_comment)
    database.commit()

    return get_comment

def update_comment(request: CommentUpdateSchema, comment_id: int, database: Session) -> Comment:
    """
        Description
        -----------
            Função que atualiza um comentário
            
        Parameters
        ----------
            request : CommentUpdateSchema
                Parâmetro com a tipagem do schema dos comentários
            comment_id : Integer
                id do comentário
        
        Return
        ------
            Comentário atualizado

    """

    get_comment = get_comment_by_id(comment_id, database)
    get_comment.comment = request.comment

    database.add(get_comment)
    database.commit()

    return get_comment
