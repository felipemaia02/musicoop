"""
    Módulo responsavel pelos métados de querys com a tabela usuário
"""
from sqlalchemy.orm import Session

from musicoop.schemas.project import ProjectSchema
from musicoop.models.project import Project
from musicoop.settings.logs import logging

logger = logging.getLogger(__name__)

def get_projects(database: Session) -> Project:
    """
      Description
      -----------

      Parameters
      ----------

    """

    projects = database.query(Project).filter().first()
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

def create_music(request: ProjectSchema, database: Session) -> Project:
    """
      Description
      -----------

      Parameters
      ----------
    """
    new_project = Project(project_name=request.project_name, file=request.file, user=1)
    database.add(new_project)
    database.commit()
    logger.info("FOI CRIADO NO BANCO A SEGUINTE CONTRIBUIÇÃO: %s", new_project)
    return new_project
