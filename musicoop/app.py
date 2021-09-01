"""
Módulo responsável por configurações da aplicação e do uvicorn
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from musicoop.database import Base, engine
from musicoop.settings.logs import logging

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


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=origins,
    allow_headers=origins,
)

try:
    Base.metadata.create_all(engine)
except Exception as error: # pylint: disable=broad-except
    logger.info("NÃO FOI POSSÍVEL CRIAR AS TABELAS NO BANCO DE DADOS AUTOMATICAMENTE: %s", error)
