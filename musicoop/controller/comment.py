"""
    Módulo responsavel pelos métados de querys com a tabela usuário
"""
from sqlalchemy.orm import Session
from typing import List
from musicoop import database
from musicoop.schemas.comment import CommentSchema
from musicoop.models.comment import Comment
from musicoop.settings.logs import logging

logger = logging.getLogger(__name__)

def get_comment_by_project(project_id:int,database: Session) -> Comment:
    """
      Description
      -----------

      Parameters
      ----------

    """
    comment = database.query(Comment).filter(Comment.project == project_id).first()
    logger.info("FOI RETORNADO DO BANCO AS SEGUINTES COMENTÁRIOS: %s", comment)

    return comment

def create_comment(request: CommentSchema, database: Session) -> Comment:
    """
      Description
      -----------

      Parameters
      ----------

    """

    new_comment = Comment()
    database.add(new_comment)
    database.commit()
    logger.info("FOI CRIADO NO BANCO A SEGUINTE CONTRIBUIÇÃO: %s", new_comment)
    return new_comment
