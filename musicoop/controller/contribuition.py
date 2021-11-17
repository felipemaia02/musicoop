"""
    Módulo responsavel pelos métados de querys com a tabela contribuition
"""
from typing import List
from sqlalchemy.orm import Session
from musicoop.schemas.contribuition import ContribuitionSchema
from musicoop.models.contribuition import Contribuition
from musicoop.settings.logs import logging

logger = logging.getLogger(__name__)


def get_contribuitions_by_post(post_id: int, database: Session) -> List:
    """
      Description
      -----------
        Função que retorna as contribuiçõe atreladas a uma publicação

      Parameters
      ----------
        post_id : Integer
          id da publicação

      Return
      ------
        Lista com as contribuições relacionadas ao post
    """
    contribuition = database.query(Contribuition).filter(
        Contribuition.post == post_id).all()
    logger.info(
        "FOI RETORNADO DO BANCO AS SEGUINTES CONTRIBUIÇÕES: %s", contribuition)

    return contribuition


def get_contribuition_by_id(contribuition_id: int, database: Session) -> Contribuition:
    """
      Description
      -----------
        Função de pega uma contribuição específica

      Parameters
      ----------
        contribuition_id : Integer
          id da contribuição

      Return
      ------
        Contribuição

    """
    contribuition = database.query(Contribuition).filter(
        Contribuition.id == contribuition_id).first()

    logger.info(
        "FOI RETORNADO DO BANCO AS SEGUINTES CONTRIBUIÇÕES: %s", contribuition)

    return contribuition


def create_contribuition(request: ContribuitionSchema,
                         database: Session) -> Contribuition:
    """
      Description
      -----------
        Função que cria a contribuição

      Parameters
      ----------
        request : ContribuitionSchema
          Parâmetro com a tipagem do schema das Contribuições
        current_user : Integer
          Usuário logado

      Return
      ------
        Nova contribuição

    """
    new_contribuition = Contribuition(name=request.name, file=request.file,
                                      post=request.post, user=request.user, file_size=request.file_size,
                                      description=request.description, username=request.username)
    database.add(new_contribuition)
    database.commit()
    if Contribuition.file is None:
        logger.info("NÃO FOI ENVIADO NENHUM ARQUIVO NESTA CONTRIBUIÇÃO")
    logger.info("FOI CRIADO NO BANCO A SEGUINTE CONTRIBUIÇÃO: %s",
                new_contribuition)
    return new_contribuition


def delete_contribuition(contribuition_id: int, database: Session) -> Contribuition:
    """
      Description
      -----------
        Função que deleta uma contribuição

      Parameters
      ----------
        contribuition_id : Integer
          id da contribuição

      Return
      ------
        Contribuição

    """
    get_contribuition = get_contribuition_by_id(contribuition_id, database)

    database.delete(get_contribuition)
    database.commit()

    return get_contribuition
