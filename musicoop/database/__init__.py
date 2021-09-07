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
    engine = create_engine('postgresql://postgres:root@localhost/musicoop',
                           encoding="utf-8",pool_pre_ping=True)
    SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

    if not database_exists(engine.url):
        logger.info("A BASE DE DADOS NÃO EXISTE. TENTANDO CRIAR...")
        create_database('postgresql://postgres:root@localhost/musicoop')

    logger.info("INICIALIZANDO TABELAS")
    Base.metadata.create_all(engine)

except AttributeError as error:
    logger.info("OCORREU ALGUM ERRO DURANTE A CRIAÇÃO DO BANCO DE DADOS: %s", error)

except Exception as error: # pylint: disable=broad-except
    logger.info("OCORREU ALGUM ERRO DURANTE A EXECUÇÃO DE QUERY BANCO DE DADOS: %s", error)


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
            logger.info("OCORREU ALGUM ERRO DURANTE A EXECUÇÃO DE QUERY BANCO DE DADOS: %s", err)
        finally:
            database.close()
    except Exception as err:  # pylint: disable=broad-except
        logger.info("OCORREU ALGUM ERRO DURANTE A EXECUÇÃO DE QUERY BANCO DE DADOS: %s", err)
