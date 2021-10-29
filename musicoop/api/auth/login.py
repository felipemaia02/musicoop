"""
Módulo responsável por ações de login e obtenção do token do usuário
"""

from os import name
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi_login.exceptions import InvalidCredentialsException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.session import Session
from starlette import status


from musicoop.settings.logs import logging
from musicoop.database import get_db
from musicoop.schemas.token import TokenSchema
from musicoop.schemas.user import UserSchema, CreateUserSchema, GetUserSchema
from musicoop.controller.user import get_user, create_user, get_user_by_id
from musicoop.utils.login import create_access_token
from musicoop.core import auth

logger = logging.getLogger(__name__)
router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
load_dotenv()


@router.get("/auth/token", status_code=status.HTTP_200_OK)
def check_logged_in(
    incoming_token: str = Depends(oauth2_scheme),
    current_user=Depends(auth.get_current_user),
    database: Session = Depends(get_db)
) -> dict:
    """
        Description
        -----------
            Função responsável por buscar instância do usuário a partir do email informada.

        Parameters
        ----------
            current_user : str
                email do usuário que deseja buscar no banco de dados.

        Returns
        -------
            Dicionário com usuário logado.
    """
    user_token = get_user(current_user.email, database).access_token
    if incoming_token != user_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido!",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {'success': current_user}


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
def register_user(request: CreateUserSchema, database: Session = Depends(get_db)) -> UserSchema:
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
    try:
        new_user = create_user(request, database)
    except IntegrityError as err:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Email ou Usuário já cadastrado"
        ) from err

    if new_user is None:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Erro ao criar o usuário no banco de dados"
        )
    return UserSchema.parse_obj({
        "email": request.email,
        "username": request.username,
        "name": request.name
    })


@router.get('/user', status_code=status.HTTP_200_OK)
def get_user(id: int, database: Session = Depends(get_db)) -> GetUserSchema:
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
    user = get_user_by_id(id, database)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_202_ACCEPTED,
            detail="retornou vazio"
        )

    return GetUserSchema.parse_obj({
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "username": user.username
    })
