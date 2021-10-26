"""
    Modulo
"""
import shutil
import os
from fastapi import UploadFile
from musicoop.settings.logs import logging


logger = logging.getLogger(__name__)

async def copy_file(file: UploadFile, type: str) -> bool:
    """
        Description
        -----------

        Parameters
        ----------
    """
    try:
        with open( "musicoop/static/" + type + file.filename, "wb") as buffer:
            logger.info("ARQUVO COPIADO COM SUCESSO PARA O DIRETÓRIO")
            shutil.copyfileobj(file.file, buffer)
            file_size = os.path.getsize("musicoop/static/" + type + file.filename)

    except Exception as err:# pylint: disable=broad-except
        logger.info("NÃO FOI POSSIVEL ENVIAR O PARA O DIRETORIO: %s", err)

        return False

    finally:
        logger.info("FECHANDO DIRETÓRIO")
        await file.close()

    return True, file_size

def validate_size(max_size: int, file: UploadFile):
    """
        Description
        -----------

        Parameters
        ----------
    """
    real_file_size = 0
    for chunk in file.file:
        real_file_size += len(chunk)
        if real_file_size > max_size:
            logger.info("ARQUIVO PASSOU DO TAMANHO PERMITIDO")
            return False
    file.file.seek(0)
    logger.info("ARQUIVO POSSUI TAMANHO PERMITIDO")
    return True, real_file_size

async def delete_file(file: UploadFile, type: str) -> bool:
    """
        Description
        -----------

        Parameters
        ----------
    """
    try:
        with open("musicoop/static/" + type + file.filename, "wb"):
            os.remove("musicoop/static/" + type + file.filename)
    except Exception as err:# pylint: disable=broad-except
        logger.info("NÃO FOI POSSIVEL REMOVER O PARA O DIRETORIO: %s", err)

        return False
    finally:
        logger.info("FECHANDO DIRETÓRIO")
        await file.close()

    return True
