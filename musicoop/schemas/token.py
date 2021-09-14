"""
    Módulo com o schema do token de acesso
"""

from musicoop.schemas.base_schema import BaseSchema

class TokenSchema(BaseSchema):
    """
        Classe que contém os atributos de um token
    """
    access_token: str
    token_type: str
