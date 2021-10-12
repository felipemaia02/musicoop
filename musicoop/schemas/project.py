"""
    Módulo com o schema do usuário
"""

from musicoop.schemas.base_schema import BaseSchema


class ProjectSchema(BaseSchema):
    """
        Classe que contém os atributos de um projeto
    """
    music_name: str
    file: str
    user : int

class GetProjectSchema(ProjectSchema):
    """
        Classe que contém os atributos de um projeto
    """
    id: int
    creation_date: str
