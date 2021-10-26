"""
Módulo responsável por configurações básicas de um Schema
"""
from pydantic import BaseModel

class BaseSchema(BaseModel):
    """
    Classe que contém as configurações básicas de um Schema
    """
    # pylint: disable=too-few-public-methods
    class Config:
        """
        Classe de configuração que habilita o modo orm para evitar error no pydantic
        """
        orm_mode = True
