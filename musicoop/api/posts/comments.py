"""
Módulo responsável por ações de login e obtenção do token do usuário
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

@router.get("/comments/{post_id}", status_code=status.HTTP_200_OK)
def get_comments(post_id : int ,db_session: Session = Depends(get_db)) -> GetCommentSchema:
    """
        Description
        -----------
        Parameters
        ----------
        Returns
        -------
        Raises
        ------
    """

    comments = get_comment_by_post(post_id, db_session)

    if not comments:
        raise HTTPException(
        status_code=status.HTTP_202_ACCEPTED,
        detail="retornou vazio"
    )

    return comments

@router.post("/comments", status_code=status.HTTP_200_OK)
def new_comments(request : CommentSchema ,db_session: Session = Depends(get_db)) -> CommentSchema:
    """
        Description
        -----------
        Parameters
        ----------
        Returns
        -------
        Raises
        ------
    """

    comments = create_comment(request, 1,db_session)

    if comments is None:
        raise HTTPException(
        status_code=status.HTTP_406_NOT_ACCEPTABLE,
        detail="Erro ao criar o comentário no banco de dados"
    )

    return CommentSchema.parse_obj({
        "post":request.post,
        "comment":request.comment,
        })

@router.delete("/comments/{comment_id}", status_code=status.HTTP_200_OK)
def delete_comments(comment_id: int, db_session: Session = Depends(get_db)) -> CommentSchema:
    """
        Description
        -----------
        Parameters
        ----------
        Returns
        -------
        Raises
        ------
    """

    deleted_comment = delete_comment(comment_id, db_session)
    if deleted_comment is None:
        raise HTTPException(
        status_code=status.HTTP_406_NOT_ACCEPTABLE,
        detail="Erro ao deletar o comentário no banco de dados"
        )

    return deleted_comment

@router.put("/comments/{comment_id}", status_code=status.HTTP_200_OK)
def update_routes(comment_id:int,
                  request: CommentUpdateSchema,
                  db_session: Session = Depends(get_db)) -> CommentUpdateSchema:
    """
        Description
        -----------
        Parameters
        ----------
        Returns
        -------
        Raises
        ------
    """
    upated_comment = update_comment(request, comment_id, db_session)

    if upated_comment is None:
        raise HTTPException(
        status_code=status.HTTP_406_NOT_ACCEPTABLE,
        detail="Erro ao atualizar o comentário no banco de dados"
        )

    return CommentUpdateSchema.parse_obj({
        "comment":request.comment,
        })
