"""
Módulo responsável pela configuração de rotas de postagem
"""
from fastapi import APIRouter
from musicoop.api.posts import post, comments

api_router = APIRouter()
api_router.include_router(post.router, tags=['post'])
api_router.include_router(comments.router, tags=['comments'])
