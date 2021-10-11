"""
Módulo responsável por ações de login e obtenção do token do usuário
"""
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm.session import Session
from starlette import status

from musicoop.settings.logs import logging
from musicoop.database import get_db
from musicoop.schemas.music import GetMusicSchema, MusicSchema
from musicoop.controller.music import get_musics, create_music

logger = logging.getLogger(__name__)
router = APIRouter()
load_dotenv()

@router.post("/musics", status_code=status.HTTP_200_OK)
def get_music(db_session: Session = Depends(get_db)) -> GetMusicSchema:
    """
        Description
        -----------
        Parameters
        ----------
        Returns
        -------
        Raises
        ------
    """

    musics = get_musics(db_session)

    if not musics:
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Erro buscar"
    )

    return musics

@router.post('/music', status_code=status.HTTP_200_OK)
def register_user(request: MusicSchema, db_session: Session = Depends(get_db)) -> MusicSchema:
    """
        Description
        -----------
        Parameters
        ----------
        Returns
        -------
        Raises
        ------
    """

    new_music = create_music(request, db_session)

    if new_music is None:
        raise HTTPException(
        status_code=status.HTTP_406_NOT_ACCEPTABLE,
        detail="Erro ao criar o usuário no banco de dados"
    )
    music = MusicSchema.parse_obj({
        "music_name": request.music_name,
        "file": request.file,
        "user": 1
    })
    return music
