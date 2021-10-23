"""
    Módulo com o schema do usuário
"""

from musicoop.schemas.base_schema import BaseSchema


class PostSchema(BaseSchema):
    """
        Classe que contém os atributos de um projeto
    """
    post_name: str
    file: str
    file_size: int
    user : int
class GetPostSchema(PostSchema):
    """
        Classe que contém os atributos de um projeto
    """
    id: int
    creation_date: str

class PostCommentSchema(GetPostSchema):
    """
        Classe que contém os atributos de um projeto
    """

    comments: list
