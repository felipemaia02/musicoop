"""
    Model responsável por salvar usuários da aplicação
"""
from musicoop.schemas.base_schema import BaseSchema


class CommentSchema(BaseSchema):
    """
        Classe que contém os atributos de um projeto
    """
    project: int
    comment: str

class GetCommentSchema(CommentSchema):
    """
        Classe que contém os atributos de um projeto
    """
    id: int
    creation_date: str
    user: int
