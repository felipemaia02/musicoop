"""
    Módulo com o schema da publicação
"""

from musicoop.models.contribuition import Contribuition
from musicoop.schemas.base_schema import BaseSchema


class PostSchema(BaseSchema):
    """
        Classe que contém os atributos de uma publicação
    """
    post_name: str
    file: str
    file_size: int
    description : str
    user : int
class GetPostSchema(PostSchema):
    """
        Classe que contém os atributos de uma publicação
    """
    id: int
    creation_date: str

class PostCommentSchema(GetPostSchema):
    """
        Classe que contém os atributos de uma publicação
    """

    comments: list
    contribuitions : list
