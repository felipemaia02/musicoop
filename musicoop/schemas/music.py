"""
    Módulo com o schema do usuário
"""

from musicoop.schemas.base_schema import BaseSchema


class MusicSchema(BaseSchema):
    """
        Classe que contém os atributos de um Usuário
    """
    music_name: str
    file: str
    user : int

class GetMusicSchema(MusicSchema):
    """
        Classe que contém os atributos de um Usuário
    """
    id: int
    creation_date: str
