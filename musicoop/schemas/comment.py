"""
    Model responsável por salvar usuários da aplicação
"""
from musicoop.schemas.base_schema import BaseSchema


class CommentSchema(BaseSchema):
    """
        Classe que contém os atributos para criar um comentário
    """
    post: int
    comment: str

class GetCommentSchema(CommentSchema):
    """
        Classe que contém os atributos de um comentário
    """
    id: int
    creation_date: str
    user: int

class CommentUpdateSchema(BaseSchema):
    """
        Classe que contém os atributos atualizar um comentário
    """
    comment: str
