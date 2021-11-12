"""
Módulo responsável por ações de comentários nos posts
"""
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm.session import Session
from starlette import status

from musicoop.settings.logs import logging
from musicoop.database import get_db
from musicoop.schemas.comment import GetCommentSchema, CommentSchema, CommentUpdateSchema
from musicoop.controller.comment import (create_comment, get_comment_by_post,
                                         delete_comment, update_comment)
# from musicoop.core.auth import get_current_user

logger = logging.getLogger(__name__)
router = APIRouter()
load_dotenv()

@router.get("/comment", status_code=status.HTTP_200_OK)
def get_comments(post_id : int ,database: Session = Depends(get_db)) -> GetCommentSchema:
    """
        Description
        -----------
            Retorna todos os comentários do post especificado pelo id
            
        Parameters
        ----------
            post_id : Integer
                id do post o qual os comentários serão retornados
        Return
                ------
                    Lista com os comentários
        
        Raises
        -------
            HTTPException - retornou vazio - HTTP_202_ACCEPTED      
    """

    comments = get_comment_by_post(post_id, database)

    if not comments:
        raise HTTPException(
        status_code=status.HTTP_202_ACCEPTED,
        detail="retornou vazio"
    )

    return comments

@router.post("/comments", status_code=status.HTTP_200_OK)
def new_comments(request : CommentSchema ,database: Session = Depends(get_db)) -> CommentSchema:
    """
        Description
        -----------
            Função que registra novos comentários
            
        Parameters
        ----------
            request : CommentSchema
                Parâmetro com a tipagem do schema dos comentários
                
        Return
        -------
            dicionário com o post onde o comentario será atrelado e o próprio comentário
        
        Raises
        ------
            HTTPException - Erro ao criar o comentário no banco de dados - HTTP_406_NOT_ACCEPTABLE
    """

    comments = create_comment(request, 1,database)

    if comments is None:
        raise HTTPException(
        status_code=status.HTTP_406_NOT_ACCEPTABLE,
        detail="Erro ao criar o comentário no banco de dados"
    )

    return CommentSchema.parse_obj({
        "post":request.post,
        "comment":request.comment,
        })

@router.delete("/comments", status_code=status.HTTP_200_OK)
def delete_comments(comment_id: int, database: Session = Depends(get_db)) -> CommentSchema:
    """
        Description
        -----------
            Função que deleta um comentário específico pelo id
            
        Parameters
        ----------
            comment_id : Integer
                id do comentário a ser deletado
                
        Returns
        -------
            Comentário deletado
            
        Raises
        ------
            HTTPException - Erro ao deletar o comentário no banco de dados - HTTP_406_NOT_ACCEPTABLE
    """

    deleted_comment = delete_comment(comment_id, database)
    if deleted_comment is None:
        raise HTTPException(
        status_code=status.HTTP_406_NOT_ACCEPTABLE,
        detail="Erro ao deletar o comentário no banco de dados"
        )

    return deleted_comment

@router.put("/comments", status_code=status.HTTP_200_OK)
def update_routes(comment_id:int,
                  request: CommentUpdateSchema,
                  database: Session = Depends(get_db)) -> CommentUpdateSchema:
    """
        Description
        -----------
            edita um comentário pelo id
        Parameters
        ----------
            comment_id : Integer
                id do comentário
            request : CommentUpdateSchema
                Parâmetro com a tipagem do schema dos comentários
        Returns
        -------
            dicionário com o comentário a editado
        Raises
        ------
            HTTPException - Erro ao atualizar o comentário no banco de dados - HTTP_406_NOT_ACCEPTABLE
    """
    upated_comment = update_comment(request, comment_id, database)

    if upated_comment is None:
        raise HTTPException(
        status_code=status.HTTP_406_NOT_ACCEPTABLE,
        detail="Erro ao atualizar o comentário no banco de dados"
        )

    return CommentUpdateSchema.parse_obj({
        "comment":request.comment,
        })
