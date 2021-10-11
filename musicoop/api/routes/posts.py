"""
Módulo responsável pela configuração de rotas de postagem
"""
from fastapi import APIRouter
from musicoop.api.posts import music

api_router = APIRouter()
api_router.include_router(music.router, tags=['posts'])
