from musicoop.schemas.base_schema import BaseSchema

class UserSchema(BaseSchema):
    """
        Classe que contém os atributos de um Usuário
    """
    email: str
    name : str
