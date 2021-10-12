"""
Módulo responsável por ações de login e obtenção do token do usuário
"""
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm.session import Session
from starlette import status

from musicoop.settings.logs import logging
from musicoop.database import get_db
from musicoop.schemas.project import GetProjectSchema, ProjectSchema
from musicoop.controller.project import get_musics, create_music, get_music_by_name

logger = logging.getLogger(__name__)
router = APIRouter()
load_dotenv()

@router.post("/projects", status_code=status.HTTP_200_OK)
def get_project(db_session: Session = Depends(get_db)) -> GetProjectSchema:
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
        status_code=status.HTTP_202_ACCEPTED,
        detail="retornou vazio"
    )

    return musics

@router.post('/project', status_code=status.HTTP_200_OK)
def new_project(request: ProjectSchema, db_session: Session = Depends(get_db)) -> ProjectSchema:
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

    validate_music = get_music_by_name(request.music_name, db_session)
    if validate_music is not None:
        raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail="Essa musica já foi cadastrada no banco de dados"
    )
    new_music = create_music(request, db_session)
    if new_music is None:
        raise HTTPException(
        status_code=status.HTTP_406_NOT_ACCEPTABLE,
        detail="Erro ao criar a música no banco de dados"
    )
    music = ProjectSchema.parse_obj({
        "music_name": request.music_name,
        "file": request.file,
        "user": 1
    })

    return music
