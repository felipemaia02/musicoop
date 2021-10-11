"""
    Módulo responsavel pelos métados de querys com a tabela usuário
"""
from sqlalchemy.orm import Session

from musicoop.schemas.music import MusicSchema, GetMusicSchema
from musicoop.models.music import Music
from musicoop.settings.logs import logging

logger = logging.getLogger(__name__)

def get_musics(database: Session) -> Music:
    """
      Description
      -----------

      Parameters
      ----------

    """

    musics = database.query(Music).filter().first()
    logger.info("FOI RETORNADO DO BANCO AS SEGUINTES CONTRIBUIÇÕES: %s", musics)

    return musics

def get_music_by_name(music_name:str, database: Session) -> Music:
    """
        Description
        -----------

        Parameters
        ----------
    """
    musics = database.query(Music).filter(Music.music_name == music_name).first()
    logger.info("FOI RETORNADO DO BANCO AS SEGUINTES CONTRIBUIÇÕES: %s", musics)

    return musics

def create_music(request: MusicSchema, database: Session) -> Music:
    """
      Description
      -----------

      Parameters
      ----------
    """
    new_music = Music(music_name=request.music_name, file=request.file, user=1)
    database.add(new_music)
    database.commit()
    logger.info("FOI CRIADO NO BANCO A SEGUINTE CONTRIBUIÇÃO: %s", new_music)
    return new_music
