"""
Módulo responsável pela configuração de rotas de postagem
"""
from fastapi import APIRouter
from musicoop.api.posts import project, comments

api_router = APIRouter()
api_router.include_router(project.router, tags=['project'])
api_router.include_router(comments.router, tags=['comments'])
