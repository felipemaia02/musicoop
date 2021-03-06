"""
Módulo responsável por configurações da aplicação e do uvicorn
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from musicoop.database import Base, engine
from musicoop.settings.logs import logging
from musicoop.api.routes import auth, posts

logger = logging.getLogger(__name__)
app = FastAPI(title="Musicoop", description="")


@app.get("/", tags=["Musicoop"])
async def root():
    """
    Rota root da API do MusiCoop
    Returns
    -------
      dict: Dicionário contendo a versão da aplicação
    """
    return {"Musicoop": "v0.1.0"}


origins = ["*", "ec2-52-207-47-210.compute-1.amazonaws.com"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=origins,
    allow_headers=origins,
)

app.include_router(auth.api_router)
app.include_router(posts.api_router)

try:
    Base.metadata.create_all(engine)
except Exception as error:  # pylint: disable=broad-except
    logger.info(
        "Não foi possível criar as tabelas no Banco de Dados automaticamente: %s", error)
