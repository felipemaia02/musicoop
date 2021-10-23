"""
Módulo responsável por ações de login e obtenção do token do usuário
"""
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Header
from fastapi.responses import StreamingResponse
from sqlalchemy.orm.session import Session
from starlette import status

from musicoop.settings.logs import logging
from musicoop.database import get_db
from musicoop.schemas.project import ProjectSchema, ProjectCommentSchema
# from musicoop.schemas.user import GetUserSchema
from musicoop.controller.project import (get_projects, create_project,
                                         get_project_by_id)
from musicoop.controller.comment import get_comment_by_project
# from musicoop.core.auth import get_current_user
from musicoop.utils.save_file import copy_file
from musicoop.utils.streamming import iterfile

logger = logging.getLogger(__name__)
router = APIRouter()
CHUNK_SIZE = 1024*1024
load_dotenv()

@router.get("/projects", status_code=status.HTTP_200_OK)
def get_project(db_session: Session = Depends(get_db)) -> ProjectCommentSchema:
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
    projects = get_projects(db_session)

    if not projects:
        raise HTTPException(
        status_code=status.HTTP_202_ACCEPTED,
        detail="retornou vazio"
    )

    list_projects = []
    for project in projects:
        comment = get_comment_by_project(project.id, db_session)
        list_projects.append(ProjectCommentSchema.parse_obj({
        "id" : project.id,
        "project_name" : project.project_name,
        "file" : project.file,
        "file_size": project.file_size,
        "user" : project.user,
        "creation_date" : str(project.creation_date),
        "comments": comment
        }))

    return list_projects

@router.get("/projects/{project_id}", status_code=status.HTTP_200_OK)
def getting_project_by_id(project_id:int,
                          db_session: Session = Depends(get_db)) -> ProjectCommentSchema:
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
    project = get_project_by_id(project_id, db_session)
    comment = get_comment_by_project(project_id, db_session)

    if project is None:
        raise HTTPException(
        status_code=status.HTTP_406_NOT_ACCEPTABLE,
        detail="Erro ao buscar projeto"
    )

    return ProjectCommentSchema.parse_obj({
        "id" : project.id,
        "project_name" : project.project_name,
        "file" : project.file,
        "file_size": project.file_size,
        "user" : project.user,
        "creation_date" : str(project.creation_date),
        "comments": comment
    })

@router.post('/projects', status_code=status.HTTP_200_OK)
async def new_project(
                project_name: str = Form(...),
                file: UploadFile = File(...),
                # current_user:GetUserSchema = Depends(get_current_user),
                db_session: Session = Depends(get_db)
                ) -> ProjectSchema:
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
    save_file, file_size = await copy_file(file)
    request = ProjectSchema.parse_obj({
        "project_name":project_name,
        "file":file.filename,
        "file_size": file_size,
        "user":1
    })
    if save_file is False:
        raise HTTPException(
        status_code=status.HTTP_406_NOT_ACCEPTABLE,
        detail="Erro ao salvar o arquivo no servidor, tente novamente!"
    )
    project = create_project(request, db_session)
    if project is None:
        raise HTTPException(
        status_code=status.HTTP_406_NOT_ACCEPTABLE,
        detail="Erro ao criar a música no banco de dados"
    )

    return request

@router.get('/musics/{project_id}')
def streamming_music(project_id:int,
                     db_session: Session = Depends(get_db),
                     range: str = Header(None)):
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
    project = get_project_by_id(project_id, db_session)
    if project is None:
        raise HTTPException(
        status_code=status.HTTP_406_NOT_ACCEPTABLE,
        detail="Erro ao reproduzir a música"
    )

    if range is None:
        start, end = CHUNK_SIZE, project.file_size
        if start > end:
            start, end = 0, CHUNK_SIZE
    else:
        start, end = range.replace("bytes=", "").split("-")
    start = int(start)
    end = int(end) if end else start + CHUNK_SIZE
    headers = {
            'Accept-Ranges': 'bytes',
            'Content-Range': f'bytes {str(start)}-{str(end)}/{project.file_size}',
        }

    return StreamingResponse(iterfile(project.file, start, end),
                            headers=headers,
                            media_type="audio/mp3",
                            status_code=status.HTTP_206_PARTIAL_CONTENT)
