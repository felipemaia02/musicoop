"""
Módulo responsável por ações das contribuições nos posts
"""
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, File, Form, UploadFile
from fastapi.responses import StreamingResponse
from sqlalchemy.orm.session import Session
from starlette import status

from musicoop.settings.logs import logging
from musicoop.database import get_db
from musicoop.utils.save_file import copy_file
from musicoop.schemas.contribuition import GetContribuitionSchema, ContribuitionSchema
from musicoop.controller.contribuition import (
    create_contribuition, get_contribuitions_by_post, delete_contribuition)
from musicoop.core.auth import get_current_user
from musicoop.schemas.user import GetUserSchema

logger = logging.getLogger(__name__)
router = APIRouter()
load_dotenv()


@router.get("/contribuition", status_code=status.HTTP_200_OK)
def get_contribuitions(post_id: int,
                       current_user: GetUserSchema = Depends(get_current_user),
                       database: Session = Depends(get_db)) -> GetContribuitionSchema:
    """
        Description
        -----------
            Retorna todos as contribuições do post especificado pelo id

        Parameters
        ----------
            post_id : Integer
                id do post o qual os comentários serão retornados
        Return
        ------
            Lista com as contribuições

        Raises
        -------
            HTTPException - retornou vazio - HTTP_202_ACCEPTED

    """

    contribuitions = get_contribuitions_by_post(post_id, database)

    if not contribuitions:
        raise HTTPException(
            status_code=status.HTTP_202_ACCEPTED,
            detail="retornou vazio"
        )

    return contribuitions


@router.post("/contribuitions", status_code=status.HTTP_200_OK)
async def new_contribuitions(post_id: int,
                             name: str = Form(...),
                             description: str = Form(...),
                             file: UploadFile = File(None),
                             current_user: GetUserSchema = Depends(
                                 get_current_user),
                             database: Session = Depends(get_db)
                             ) -> ContribuitionSchema:
    """
        Description
        -----------
            Função que cria uma nova contribuição
        Parameters
        ----------
            post_id : Integer
                Id do post o qual será atrelado a contribuição
            name : String
                Nome da contribuição
            description : String
                Descrição da contribuição
            file : UploadFile
                Arquivo de áudio da contribuição

        Returns
        -------
            Dicionário com os parêmetros da contribuição

        Raises
        ------
            HTTPException - Arquivo não é valido, apenas mp3! - HTTP_415_UNSUPPORTED_MEDIA_TYPE
            HTTPException - Erro ao salvar o arquivo no servidor, tente novamente! - HTTP_417_EXPECTATION_FAILED
            HTTPException - Erro ao criar o comentário no banco de dados - HTTP_406_NOT_ACCEPTABLE
    """
    if file is not None:
        if file.content_type != "audio/mp3" and file.content_type != "audio/mpeg":
            raise HTTPException(
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                detail="Arquivo não é valido, apenas mp3!"
            )
        save_file, file_size = await copy_file(file, "contribuition/")

        if save_file is False:
            raise HTTPException(
                status_code=status.HTTP_417_EXPECTATION_FAILED,
                detail="Erro ao salvar o arquivo no servidor, tente novamente!"
            )

    request = ContribuitionSchema.parse_obj({
        "name": name,
        "file": file.filename if file is not None else "",
        "file_size": file_size if file is not None else 0,
        "description": description,
        "post": post_id,
        "user": current_user.id,
        "username": current_user.username,
        "aproved": True
    })
    contribuitions = create_contribuition(request, database)

    if contribuitions is None:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Erro ao criar o comentário no banco de dados"
        )

    return request


@router.delete("/contribuitions", status_code=status.HTTP_200_OK)
def delete_contribuitions(contribuition_id: int,
                          current_user: GetUserSchema = Depends(
                              get_current_user),
                          database: Session = Depends(get_db)) -> ContribuitionSchema:
    """
        Description
        -----------
            Função que deleta a contribuição

        Parameters
        ----------
            contribuition_id : Integer

        Returns
        -------
            Contribuição deletada

        Raises
        ------
            HTTPException - Erro ao deletar o comentário no banco de dados - HTTP_406_NOT_ACCEPTABLE
    """

    deleted_contribuition = delete_contribuition(contribuition_id, database)
    if deleted_contribuition is None:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Erro ao deletar o comentário no banco de dados"
        )

    return deleted_contribuition

# @router.put("/contribuitions", status_code=status.HTTP_200_OK)
# def update_routes(contribuition_id:int,
#                   request: ContribuitionUpdateSchema,
    # current_user: GetUserSchema = Depends(
    #                                  get_current_user),
#                   database: Session = Depends(get_db)) -> ContribuitionUpdateSchema:
#     """
#         Description
#         -----------
#         Parameters
#         ----------
#         Returns
#         -------
#         Raises
#         ------
#     """
#     upated_contribuition = update_contribuition(request, contribuition_id, database)

#     if upated_contribuition is None:
#         raise HTTPException(
#         status_code=status.HTTP_406_NOT_ACCEPTABLE,
#         detail="Erro ao atualizar o comentário no banco de dados"
#         )

#     return ContribuitionUpdateSchema.parse_obj({
#         "contribuition":request.contribuition,
#         })
