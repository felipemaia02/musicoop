"""
Módulo responsável por ações de login e obtenção do token do usuário
"""
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi_login.exceptions import InvalidCredentialsException
from sqlalchemy.orm.session import Session
from starlette import status

from musicoop.settings.logs import logging
from musicoop.database import get_db
from musicoop.schemas.token import TokenSchema
from musicoop.schemas.user import UserSchema, CreateUserSchema
from musicoop.controller.user import get_user, create_user
from musicoop.utils.login import create_access_token
from musicoop.core import auth