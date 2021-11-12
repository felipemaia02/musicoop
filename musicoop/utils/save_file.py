"""
    Modulo
"""
import shutil
import os
from fastapi import UploadFile
from sqlalchemy.sql.expression import true
from musicoop.settings.logs import logging
from dotenv import load_dotenv
from botocore.exceptions import ClientError
from musicoop.utils.aws_connection import connection_aws

load_dotenv()

logger = logging.getLogger(__name__)


async def copy_file(file: UploadFile, type: str) -> bool:
    """
        Description
        -----------

        Parameters
        ----------
    """
    try:
        path = os.getenv('MUSIC_PATH') + type + file.filename
        with open(path, "wb") as buffer:
            logger.info("ARQUVO COPIADO COM SUCESSO PARA O DIRETÓRIO")
            shutil.copyfileobj(file.file, buffer)
            file_size = os.path.getsize(path)
            if os.getenv('SERVER_TYPE') == "PROD":
                delete_all_files(os.getenv('MUSIC_PATH') + type)
                upload_file_aws(path,
                                os.getenv('BUCKET_NAME'),
                                type + file.filename)
    except Exception as err:  # pylint: disable=broad-except
        logger.info("NÃO FOI POSSIVEL ENVIAR O PARA O DIRETORIO: %s", err)
        return False
    finally:
        logger.info("FECHANDO DIRETÓRIO")
        await file.close()

    return True, file_size


def upload_file_aws(file_name, bucket, object_name=None):

    s3_client = connection_aws()
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logger.info("ARQUVO FALHOU AO SALVAR NO AWS")
        return False
    logger.info("ARQUVO SALVADO NO AWS COM SUCESSO")
    return True


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
    except Exception as err:  # pylint: disable=broad-except
        logger.info("NÃO FOI POSSIVEL REMOVER O PARA O DIRETORIO: %s", err)

        return False
    finally:
        logger.info("FECHANDO DIRETÓRIO")
        await file.close()

    return True


def delete_all_files(type: str) -> bool:
    path = os.getenv('MUSIC_PATH') + type
    try:
        for file in os.listdir(path):
            os.remove(os.path.join(path, file))
        logger.info("FOI REMOVIDOS O ARQUIVOS NO DIRETORIO")
        return True
    except Exception as err:
        logger.info("NÃO FOI POSSIVEL REMOVER O ARQUIVOS NO DIRETORIO: %s", err)
        return False
