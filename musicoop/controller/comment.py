"""
    Módulo responsavel pelos métados de querys com a tabela usuário
"""
from typing import List

from sqlalchemy.orm import Session
from musicoop.schemas.comment import CommentSchema
from musicoop.models.comment import Comment
# from musicoop.schemas.user import GetUserSchema
from musicoop.settings.logs import logging

logger = logging.getLogger(__name__)

def get_comment_by_project(project_id: int, database: Session) -> List:
    """
      Description
      -----------

      Parameters
      ----------
    """
    comment = database.query(Comment).filter(Comment.project == project_id).all()
    logger.info("FOI RETORNADO DO BANCO AS SEGUINTES COMENTÁRIOS: %s", comment)

    return comment

def create_comment(request: CommentSchema, current_user: int, database: Session) -> Comment:
    """
      Description
      -----------

      Parameters
      ----------

    """

    new_comment = Comment(user=current_user, project=request.project, comment=request.comment)
    database.add(new_comment)
    database.commit()
    logger.info("FOI CRIADO NO BANCO A SEGUINTE CONTRIBUIÇÃO: %s", new_comment)
    return new_comment
