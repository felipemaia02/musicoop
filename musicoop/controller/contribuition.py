"""
    Módulo responsavel pelos métados de querys com a tabela usuário
"""
from typing import List
from sqlalchemy.orm import Session
from musicoop.schemas.contribuition import ContribuitionSchema
from musicoop.models.contribuition import Contribuition
from musicoop.settings.logs import logging

logger = logging.getLogger(__name__)

def get_contribuitions(database: Session) -> List:
    """
      Description
      -----------

      Parameters
      ----------
    """

    contribuitions = database.query(Contribuition).order_by(Contribuition.id.desc()).all()
    logger.info("FOI RETORNADO DO BANCO AS SEGUINTES CONTRIBUIÇÕES: %s", contribuitions)

    return contribuitions

def get_project_by_name(contribuition_name:str, database: Session) -> Contribuition:
    """
        Description
        -----------

        Parameters
        ----------
    """
    contribuition = database.query(Contribuition).filter(Contribuition.name == contribuition_name).first()
    logger.info("FOI RETORNADO DO BANCO AS SEGUINTES CONTRIBUIÇÕES: %s", contribuition)

    return contribuition

def get_contribuition_by_id(contribuition_id:int, database: Session) -> Contribuition:
    """
        Description
        -----------

        Parameters
        ----------
    """
    contribuition = database.query(Contribuition).filter(Contribuition.id == contribuition_id).first()

    logger.info("FOI RETORNADO DO BANCO AS SEGUINTES CONTRIBUIÇÕES: %s", contribuition)

    return contribuition

def create_contribuition(request: ContribuitionSchema,
                   database: Session) -> Contribuition:
    """
      Description
      -----------

      Parameters
      ----------
    """
    new_contribuition = Contribuition(name=request.contribuition_name,file=request.file,
                          project=request.project,user=request.user)
    database.add(new_contribuition)
    database.commit()
    logger.info("FOI CRIADO NO BANCO A SEGUINTE CONTRIBUIÇÃO: %s", new_contribuition)
    return new_contribuition

def delete_contribuition(contribuition_id: int, database: Session) -> Contribuition:
    """
      Description
      -----------

      Parameters
      ----------
    """

    get_contribuition = get_contribuition_by_id(contribuition_id, database)

    database.delete(get_contribuition)
    database.commit()

    return get_contribuition
