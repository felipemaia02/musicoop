# import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm #OAuth2PasswordBearer
from fastapi_login.exceptions import InvalidCredentialsException
from jose import jwt
# from passlib.hash import bcrypt_sha256
from sqlalchemy.orm.session import Session
from starlette import status

from musicoop.models.user import User
from musicoop.settings.logs import logging
from musicoop.database import get_db
from musicoop.schemas.token import TokenSchema
from musicoop.schemas.user import UserSchema
from musicoop.controller.user import get_user

logger = logging.getLogger(__name__)
router = APIRouter()
load_dotenv()

def create_access_token(data: dict) -> str:
    """
      Description
      -----------

      Parameters
      ----------
    """
    expire_date = datetime.utcnow() + timedelta(minutes=int(720))
    data.update({"expire_token": str(expire_date)})
    refresh_token = jwt.encode(data, "MYKEY", algorithm="HS256")
    logger.info("REFRESH TOKEN GERADO COM SUCESSO")
    return refresh_token

@router.post("/login", status_code=status.HTTP_200_OK, response_model=TokenSchema)
def login_token(data: OAuth2PasswordRequestForm = Depends(),
                database: Session = Depends(get_db)) -> TokenSchema:
    """
      Description
      -----------

      Parameters
      ----------
    """
    email = data.username.lower()
    try:
        user = get_user(email, database)
        print(user)
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
