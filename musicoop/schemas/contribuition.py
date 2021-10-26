"""
    Módulo com o schema do usuário
"""

from musicoop.schemas.base_schema import BaseSchema


class ContribuitionSchema(BaseSchema):
    """
        Classe que contém os atributos de um projeto
    """
    name: str
    file: str
    file_size : int
    description : str
    post: int
    user : int
    aproved : bool
class GetContribuitionSchema(ContribuitionSchema):
    """
        Classe que contém os atributos de um projeto
    """
    id: int
    creation_date: str

class ContribuitionCommentSchema(GetContribuitionSchema):
    """
        Classe que contém os atributos de um projeto
    """

    comments: list
