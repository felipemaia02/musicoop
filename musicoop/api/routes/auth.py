"""
Módulo responsável pela configuração de rotas de login/acesso do usuário
"""
from fastapi import APIRouter
from musicoop.api.auth import login

api_router = APIRouter()
api_router.include_router(login.router, tags=['login'])
