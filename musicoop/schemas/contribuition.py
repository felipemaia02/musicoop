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
    project: int
    user : int
    aproved : bool
class GetProjectSchema(ContribuitionSchema):
    """
        Classe que contém os atributos de um projeto
    """
    id: int
    creation_date: str

class ContribuitionCommentSchema(GetProjectSchema):
    """
        Classe que contém os atributos de um projeto
    """

    comments: list
