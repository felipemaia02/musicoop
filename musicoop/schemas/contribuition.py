"""
    Módulo com o schema da contribuição
"""

from musicoop.schemas.base_schema import BaseSchema


class ContribuitionSchema(BaseSchema):
    """
        Classe que contém os atributos de uma contribuição
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
        Classe que contém os atributos de uma contribuição
    """
    id: int
    creation_date: str

class ContribuitionCommentSchema(GetContribuitionSchema):
    """
        Classe que contém os atributos de uma contribuição
    """

    comments: list
