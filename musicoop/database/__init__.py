"""
Módulo responsável por configurações do banco de dados
"""
import os
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from dotenv import load_dotenv
from musicoop.settings.logs import logging

logger = logging.getLogger(__name__)
Base = declarative_base()
load_dotenv()

try:
    engine = create_engine(os.getenv('SQLALCHAMY_DATABASE_URL'), encoding="utf-8",
                            pool_pre_ping=True)
    SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
    if not database_exists(engine.url):
        logger.info("A Base de Dados não existe. Tentando criar...")
        create_database(os.getenv('SQLALCHAMY_DATABASE_URL'))

    logger.info("Inicializando Tabelas")
    Base.metadata.create_all(engine)
except AttributeError as error:
    logger.info("ERRO ao criar conexão com o Banco de Dados: %s", error)
except Exception as error: # pylint: disable=broad-except
    logger.info("Ocorreu algum erro ao criar conexão com o Banco de Dados: %s", error)

def get_db() -> Generator:
    """
    Abre uma sessão para transação no Banco de Dados.
    Ao final da execução fecha a sessão.
    """
    try:
        database = SessionLocal()
        try:
            yield database
        except Exception as err:  # pylint: disable=broad-except
            logger.info("Ocorreu algum erro durante a execução de query Banco de Dados: %s", err)
        finally:
            database.close()
    except Exception as err: # pylint: disable=broad-except
        logger.info("Ocorreu algum erro durante a busca da instância do Banco de Dados: %s", err)
