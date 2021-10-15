"""
    Módulo responsavel pelos métados de querys com a tabela usuário
"""
from typing import List
from sqlalchemy.orm import Session
from musicoop.schemas.project import ProjectSchema
from musicoop.models.project import Project
from musicoop.settings.logs import logging

logger = logging.getLogger(__name__)

def get_projects(database: Session) -> List:
    """
      Description
      -----------

      Parameters
      ----------

    """

    projects = database.query(Project).all()
    logger.info("FOI RETORNADO DO BANCO AS SEGUINTES CONTRIBUIÇÕES: %s", projects)

    return projects

def get_project_by_name(project_name:str, database: Session) -> Project:
    """
        Description
        -----------

        Parameters
        ----------
    """
    project = database.query(Project).filter(Project.project_name == project_name).first()
    logger.info("FOI RETORNADO DO BANCO AS SEGUINTES CONTRIBUIÇÕES: %s", project)

    return project

def get_project_by_id(project_id:str, database: Session) -> Project:
    """
        Description
        -----------

        Parameters
        ----------
    """
    project = database.query(Project).filter(Project.id == project_id).first()
    logger.info("FOI RETORNADO DO BANCO AS SEGUINTES CONTRIBUIÇÕES: %s", project)

    return project

def create_project(request: ProjectSchema,
                   database: Session) -> Project:
    """
      Description
      -----------

      Parameters
      ----------
    """
    new_project = Project(project_name=request.project_name,file=request.file, user=request.user)
    database.add(new_project)
    database.commit()
    logger.info("FOI CRIADO NO BANCO A SEGUINTE CONTRIBUIÇÃO: %s", new_project)
    return new_project
