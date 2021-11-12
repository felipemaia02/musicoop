"""
Módulo responsável pela configuração de rotas de postagem e contribuições
"""
from fastapi import APIRouter
from musicoop.api.posts import post, comments, contribuitions

api_router = APIRouter()
api_router.include_router(post.router, tags=['post'])
api_router.include_router(contribuitions.router, tags=['contribuitions'])
api_router.include_router(comments.router, tags=['comments'])
