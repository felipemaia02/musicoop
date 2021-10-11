"""
Módulo responsável por ações de login e obtenção do token do usuário
"""
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm #OAuth2PasswordBearer
from fastapi_login.exceptions import InvalidCredentialsException
from sqlalchemy.orm.session import Session
from starlette import status

from musicoop.settings.logs import logging
from musicoop.database import get_db
from musicoop.schemas.token import TokenSchema
from musicoop.schemas.user import UserSchema, CreateUserSchema
from musicoop.controller.user import get_user, create_user
from musicoop.utils.login import create_access_token

logger = logging.getLogger(__name__)
router = APIRouter()
load_dotenv()

@router.post("/login", status_code=status.HTTP_200_OK, response_model=TokenSchema)
def login_token(data: OAuth2PasswordRequestForm = Depends(),
                database: Session = Depends(get_db)) -> TokenSchema:
    """
        Description
        -----------
            Função responsável por realizar a o login do usuário e obter o token de acesso

        Parameters
        ----------
            data : OAuth2PasswordRequestForm
                Parâmetro com as credenciais de acesso do usuário

        Returns
        -------
            Dicionário com o token e tipo de token obtidos após o login

        Raises
        ------
            InvalidCredentialsException - Caso as credenciais sejam inválidas
    """
    email = data.username.lower()
    try:
        user = get_user(email, database)
    except ConnectionError as err:
        raise HTTPException(status.HTTP_424_FAILED_DEPENDENCY) from err
    if user is None:
        logger.info("NÃO FOI POSSÍVEL LOGAR COM O USUÁRIO %s", user)
        raise InvalidCredentialsException
    logger.info("USUÁRIO %s LOGADO COM SUCESSO", email)
    access_token = create_access_token({
                                        "email": email,
                                        })

    user.access_token = access_token
    database.add(user)
    database.commit()

    return TokenSchema.parse_obj({
                                'access_token': access_token,
                                'token_type': 'bearer'
                                })

@router.post('/user', status_code=status.HTTP_200_OK)
def register_user(request: CreateUserSchema, db_session: Session = Depends(get_db)) -> UserSchema:
    """
        Description
        -----------
            Função responsável por realizar o cadastro do usuário

        Parameters
        ----------


        Returns
        -------


        Raises
        ------
    """
    new_user = create_user(request, db_session)
    #TODO: VALIDA CASO E EMAIL E USUARIO EXISTAM NÃO PERMITIR CRIAR NOVA CONTA

    if new_user is None:
        raise HTTPException(
        status_code=status.HTTP_406_NOT_ACCEPTABLE,
        detail="Erro ao criar o usuário no banco de dados"
    )
    user = UserSchema.parse_obj({
        "email": request.email,
        "username": request.username,
        "name": request.name
    })
    return user
