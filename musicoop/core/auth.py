"""
Módulo responsável por buscar as informações do usuário a partir do token informado.
"""
from datetime import datetime
import os
from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException
from sqlalchemy.orm.session import Session
from musicoop.models.user import User
from musicoop.schemas.user import GetUserSchema
from musicoop.database import get_db
from musicoop.settings.logs import logging
from musicoop.controller.user import get_user

logger = logging.getLogger(__name__)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
manager = LoginManager(os.getenv('SECRET_KEY'), "/login")


@manager.user_loader
def load_user(email: str, username: str, database: Session) -> GetUserSchema:
    """Função responsável por buscar instância do usuário a partir do Email informado.

        Parameters
        ----------
        email : str
            Email do usuário que deseja buscar no banco de dados.

        RetManagerurns
        -------
            Instância de User do schema com informações da email, nome, username do usuário
    """
    user = database.query(User).filter_by(
        email=email, username=username).one_or_none()
    if user is None:
        logger.info("NÃO FOI POSSÍVEL BUSCAR O USUÁRIO")
        raise InvalidCredentialsException
    logger.info("BUSCA DO USUÁRIO REALIZADA COM SUCESSO")
    return GetUserSchema(email=email,
                         id=user.id,
                         username=username,
                         name=user.name,
                         )


def get_current_user(token: str = Depends(oauth2_scheme),
                     database: Session = Depends(get_db)) -> GetUserSchema:
    """
        Função responsável por buscar as informações do usuário ao verificar o token.

        Parameters
        ----------
        token : str
            token de acesso do usuário que será buscada a informação

        Returns
        -------
        Instância do usuário que possui o token de acesso

        Raises
        ------
        HTTPException - caso não seja possível obter informações ou validar o token
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível obter informações do token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, os.getenv(
            'SECRET_KEY'), algorithms=["HS256"])
        token_exp = datetime.strptime(payload.get(
            "expire_token"), "%Y-%m-%d %H:%M:%S.%f")
        email: str = payload.get("email")
        username: str = payload.get("username")

        user_token = user = get_user(
            email=email, database=database).access_token
        if datetime.now() >= token_exp or token != user_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if email is None:
            raise credentials_exception

        user = load_user(email, username, database)
        return user
    except JWTError as error:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Não foi possível validar as credenciais",
        ) from error
