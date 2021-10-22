"""
    Módulo com o schema do usuário
"""

from musicoop.schemas.base_schema import BaseSchema


class ProjectSchema(BaseSchema):
    """
        Classe que contém os atributos de um projeto
    """
    project_name: str
    file: str
    file_size: int
    user : int
class GetProjectSchema(ProjectSchema):
    """
        Classe que contém os atributos de um projeto
    """
    id: int
    creation_date: str

class ProjectCommentSchema(GetProjectSchema):
    """
        Classe que contém os atributos de um projeto
    """

    comments: list
