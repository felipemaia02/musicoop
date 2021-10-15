"""
Módulo responsável por ações de login e obtenção do token do usuário
"""
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm.session import Session
from starlette import status

from musicoop.settings.logs import logging
from musicoop.database import get_db
from musicoop.schemas.comment import GetCommentSchema, CommentSchema
from musicoop.controller.comment import create_comment, get_comment_by_project
# from musicoop.core.auth import get_current_user

logger = logging.getLogger(__name__)
router = APIRouter()
load_dotenv()

@router.get("/comments/{project_id}", status_code=status.HTTP_200_OK)
def get_project(project_id : int ,db_session: Session = Depends(get_db)) -> GetCommentSchema:
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

    comments = get_comment_by_project(project_id, db_session)

    if not comments:
        raise HTTPException(
        status_code=status.HTTP_202_ACCEPTED,
        detail="retornou vazio"
    )

    return comments

@router.post("/comments", status_code=status.HTTP_200_OK)
def new_project(request : CommentSchema ,db_session: Session = Depends(get_db)) -> CommentSchema:
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
        "project":request.project,
        "comment":request.comment,
        })
