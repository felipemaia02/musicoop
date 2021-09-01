from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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
