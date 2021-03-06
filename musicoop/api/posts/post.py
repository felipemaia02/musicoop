"""
Módulo responsável por ações dos posts
"""
import os
from typing import Dict
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Header
from fastapi.responses import StreamingResponse, FileResponse
from sqlalchemy.orm.session import Session
from starlette import status

from musicoop.settings.logs import logging
from musicoop.database import get_db
from musicoop.schemas.post import PostSchema, PostCommentSchema, GetPostSchema
from musicoop.schemas.user import GetUserSchema
from musicoop.controller.post import (get_posts, create_post,
                                      get_post_by_id, get_post_by_user)
from musicoop.controller.comment import get_comment_by_post
from musicoop.controller.contribuition import get_contribuitions_by_post, get_contribuition_by_id
from musicoop.core.auth import get_current_user
from musicoop.utils.save_file import copy_file, delete_all_files
from musicoop.utils.streamming import iterfile
from musicoop.utils.aws_connection import connection_aws

logger = logging.getLogger(__name__)
router = APIRouter()
CHUNK_SIZE = 1024*1024
load_dotenv()


@router.get("/posts", status_code=status.HTTP_200_OK)
def get_post(current_user: GetUserSchema = Depends(get_current_user),
             database: Session = Depends(get_db)) -> PostCommentSchema:
    """
        Description
        -----------
            Retorna todos os posts no banco de dados

        Parameters
        ----------
            database : Session
                Sessão no banco de dados

        Returns
        -------
            Lista com todos os post no banco de dados

        Raises
        ------
            HTTPException - retornou vazio - HTTP_202_ACCEPTED
    """
    posts = get_posts(database)

    if not posts:
        raise HTTPException(
            status_code=status.HTTP_202_ACCEPTED,
            detail="retornou vazio"
        )

    list_posts = []
    for post in posts:
        contribuition = get_contribuitions_by_post(post.id, database)
        list_posts.append(PostCommentSchema.parse_obj({
            "id": post.id,
            "post_name": post.post_name,
            "file": post.file,
            "file_size": post.file_size,
            "description": post.description,
            "user": post.user,
            "creation_date": str(post.creation_date),
            "username": post.username,
            "contribuitions": contribuition
        }))

    return list_posts


@router.get("/post", status_code=status.HTTP_200_OK)
def getting_post_by_id(post_id: int,
                       current_user: GetUserSchema = Depends(get_current_user),
                       database: Session = Depends(get_db)) -> PostCommentSchema:
    """
        Description
        -----------
            Retorna um post específico pelo id

        Parameters
        ----------
            post_id : Integer
                Id do post
        Returns
        -------
            Dicionário com os parâmetros do post retornado

        Raises
        ------
            HTTPException - Erro ao buscar post - HTTP_406_NOT_ACCEPTABLE
    """
    post = get_post_by_id(post_id, database)
    contribuition = get_contribuitions_by_post(post_id, database)

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Erro ao buscar post"
        )

    return PostCommentSchema.parse_obj({
        "id": post.id,
        "post_name": post.post_name,
        "file": post.file,
        "file_size": post.file_size,
        "description": post.description,
        "user": post.user,
        "creation_date": str(post.creation_date),
        "username": post.username,
        "contribuitions": contribuition
    })


@router.post('/posts', status_code=status.HTTP_200_OK)
async def new_post(
    post_name: str = Form(...),
    description: str = Form(...),
    file: UploadFile = File(...),
    current_user: GetUserSchema = Depends(get_current_user),
    database: Session = Depends(get_db)
) -> PostSchema:
    """
        Description
        -----------
            Função que cria um novo post

        Parameters
        ----------
            post_name : String
                Nome da publicação
            description : String
                Descrição da publicação
            file : UploadFile
                Arquivo de áudio da publicação

        Returns
        -------
            Dicionário com os parâmetros da publicação

        Raises
        ------
            HTTPException - Arquivo não é valido, apenas mp3! - HTTP_415_UNSUPPORTED_MEDIA_TYPE
            HTTPException - Erro ao salvar o arquivo no servidor, tente novamente! - HTTP_417_EXPECTATION_FAILED
            HTTPException - Erro ao criar a música no banco de dados - HTTP_406_NOT_ACCEPTABLE
    """
    if file.content_type != "audio/mpeg":
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Arquivo não é valido, apenas mp3!"
        )
    save_file, file_size = await copy_file(file, "post/")

    request = PostSchema.parse_obj({
        "post_name": post_name,
        "file": file.filename,
        "description": description,
        "file_size": file_size,
        "user": current_user.id,
        "username": current_user.username
    })
    if save_file is False:
        raise HTTPException(
            status_code=status.HTTP_417_EXPECTATION_FAILED,
            detail="Erro ao salvar o arquivo no servidor, tente novamente!"
        )
    post = create_post(request, database)
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Erro ao criar a música no banco de dados"
        )

    return request


@router.get('/musics', status_code=status.HTTP_206_PARTIAL_CONTENT)
def streamming_music(post_id: int = None,
                     contribuition_id: int = None,
                     database: Session = Depends(get_db),
                     range: str = Header(None)) -> StreamingResponse:  # pylint: disable=redefined-builtin
    """
        Description
        -----------
            Função que executa o streaming de música da publicações e contribuições

        Parameters
        ----------
            post_id : Integer
                id da publicação
            contribuition_id : Integer
                id da contribuição

        Returns
        -------
            StreamingResponse
                Streaming do arquivo de áudio associado

        Raises
        ------
            HTTPException - Precisa passar um post_id ou uma contribuition_id - HTTP_422_UNPROCESSABLE_ENTITY
            HTTPException - Erro ao reproduzir a música - HTTP_406_NOT_ACCEPTABLE

    """
    if post_id is None and contribuition_id is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Precisa passar um post_id ou uma contribuition_id"
        )
    path_type = "post/"
    post = get_post_by_id(post_id, database)
    if contribuition_id:
        path_type = "contribuition/"
        post = get_contribuition_by_id(contribuition_id, database)

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Erro ao reproduzir a música"
        )
    if range is None:
        start, end = CHUNK_SIZE, post.file_size
        if start > end:
            start, end = 0, 4096
    else:
        start, end = range.replace("bytes=", "").split("-")
    start = int(start)
    end = int(end) if end else start + CHUNK_SIZE
    headers = {
        'Accept-Ranges': 'bytes',
        'Content-Range': f'bytes {str(start)}-{str(end)}/{str(post.file_size)}',
    }
    if post.file_size < CHUNK_SIZE:
        headers = {
            'Accept-Ranges': 'bytes',
            'Content-Range': f'bytes {str(0)}-{str(0)}/{str(post.file_size)}',
        }

    return StreamingResponse(iterfile(post.file, start, end, path_type),
                             headers=headers,
                             media_type="audio/mpeg",
                             status_code=status.HTTP_206_PARTIAL_CONTENT)


@router.get("/download", status_code=status.HTTP_200_OK)
async def download_file(post_id: int = None,
                        contribuition_id: int = None,
                        database: Session = Depends(get_db)) -> FileResponse:
    """
        Description
        -----------
            Função que permite fazer o download do arquivo de audio da publicação ou da contribuição

        Parameters
        ----------
            post_id : Integer
                id da publicação
            contribuicion_id : Integer
                id da contribuição

        Returns
        -------
            Arquivo de áudio a ser baixado

        Raises
        ------
            HTTPException - Precisa passar um post_id ou uma contribuition_id - HTTP_422_UNPROCESSABLE_ENTITY
    """
    if post_id is None and contribuition_id is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Precisa passar um post_id ou uma contribuition_id"
        )

    post = get_post_by_id(post_id, database)
    type_path = "post/"
    if contribuition_id:
        type_path = "contribuition/"
        post = get_contribuition_by_id(contribuition_id, database)

    if os.getenv("SERVER_TYPE") == "PROD":
        delete_all_files(type_path)
        s3_client = connection_aws()
        file_aws_path = type_path + post.file

        s3_client.download_file(os.getenv(
            "BUCKET_NAME"), file_aws_path, os.getenv("MUSIC_PATH") + file_aws_path)

    path = os.getenv("MUSIC_PATH") + type_path + post.file

    return FileResponse(path=path,
                        filename=post.file)


@router.get("/post/user", status_code=status.HTTP_200_OK)
def get_posts_by_user_auth(database: Session = Depends(get_db),
                           current_user: GetUserSchema = Depends(get_current_user)) -> PostCommentSchema:
    """
        Description
        -----------
            Função buscar um post pelo usuário


        Returns
        -------
            GetPostSchema - Schema do post

        Raises
        ------
            HTTPException - Caso o post retorne vazio HTTP_202_ACCEPTED
    """

    posts = get_post_by_user(current_user.id, database)
    list_posts = []
    for post in posts:
        contribuition = get_contribuitions_by_post(post.id, database)
        list_posts.append(PostCommentSchema.parse_obj({
            "id": post.id,
            "post_name": post.post_name,
            "file": post.file,
            "file_size": post.file_size,
            "description": post.description,
            "user": post.user,
            "creation_date": str(post.creation_date),
            "username": post.username,
            "contribuitions": contribuition
        }))

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_202_ACCEPTED,
            detail="Post veio vazio"
        )

    return list_posts
