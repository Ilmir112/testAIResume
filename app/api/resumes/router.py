from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from starlette import status

from app.api.resumes.dao import ResumesDAO, ResumesHistoryDAO
from app.api.resumes.models import ResumesHistory
from app.api.resumes.schemas import SResumes
from app.api.users.dependencies import get_current_user
from app.api.users.models import Users
from app.exceptions import CannotFindResume, ResumeStatusExistsException
from app.logger import logger

router = APIRouter(prefix="/api/resume", tags=["Данные по резюме"])


@router.get("/get_all")
async def get_resumes_all(user: Users = Depends(get_current_user)):
    try:
        result = await ResumesDAO.find_all()
        if result:
            return result
        raise CannotFindResume

    except SQLAlchemyError as e:
        logger.error(e)
    except Exception as e:
        logger.error(e)


@router.get("/get_all_by_user")
async def get_resumes_all(user: Users = Depends(get_current_user)):
    try:
        result = await ResumesDAO.find_all(user_id=user.id)
        if result:
            return result
        raise CannotFindResume

    except SQLAlchemyError as e:
        logger.error(e)
    except Exception as e:
        logger.error(e)


@router.get("/get_resume_by_id/{resume_id}")
async def get_resume_by_id(resume_id: int, user: Users = Depends(get_current_user)):
    try:
        result = await ResumesDAO.find_join(
            model=ResumesHistory,
            filter_by={"resume_id": resume_id},
            join_related="resume",
        )
        if result:
            return result

    except SQLAlchemyError as e:
        msg = f"Database Exception  {e}"
        logger.error(
            msg,
            extra={"resume_id": resume_id},
            exc_info=True,
        )
    except Exception as e:
        msg = f"Unexpected error: {str(e)}"
        logger.error(
            msg,
            extra={"resume_id": resume_id},
            exc_info=True,
        )


@router.post("/add_data")
async def add_resume_data(
    resume_data: SResumes, user: Users = Depends(get_current_user)
):
    try:
        if resume_data:
            result = await ResumesDAO.find_one_or_none(title=resume_data.title)
            if result is None:
                result = await ResumesDAO.add_with_history(resume_data, user.id)
                if result:
                    return {"status": "success", "detail": result}
        return {"status": "not success", "detail": None}

    except SQLAlchemyError as e:
        msg = f"Database Exception {e}"
        logger.error(
            msg,
            extra={"resume": resume_data.title},
            exc_info=True,
        )

    except Exception as e:
        msg = f"Unexpected error: {str(e)}"
        logger.error(
            msg,
            extra={"resume": resume_data.title},
            exc_info=True,
        )


@router.post("/{resume_id}/improve")
async def improve_resume(resume_id: int, user: Users = Depends(get_current_user)):
    try:
        resume_data = await ResumesDAO.find_one_or_none(id=resume_id)
        if resume_data:
            improved_content = await ResumesDAO.call_ai_for_improvement(
                resume_data.context
            )

            result_find = await ResumesHistoryDAO.find_one_or_none(
                resume_id=resume_data.id, context=improved_content
            )
            if result_find is None:
                new_resume_history = await ResumesHistoryDAO.add(
                    resume_id=resume_data.id, context=improved_content
                )

                return {
                    "status": status.HTTP_200_OK,
                    "detail": {"improved_content": new_resume_history.context},
                }
        raise ResumeStatusExistsException

    except SQLAlchemyError as e:
        msg = f"Database Exception {e}"
        logger.error(
            msg,
            extra={"resume_id": id},
            exc_info=True,
        )
    except Exception as e:
        msg = f"Unexpected error: {str(e)}"
        logger.error(
            msg,
            extra={"resume_id": id},
            exc_info=True,
        )


@router.put("/update/{resume_id}")
async def update_resume_data(
    resume_id: int, resume_data: SResumes, user: Users = Depends(get_current_user)
):

    result = await ResumesDAO.update(
        filter_by={"id": resume_id},
        title=resume_data.title,
        context=resume_data.context,
    )
    if result:
        return result
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Резюме не найдено"
    )


@router.delete("/delete/{resume_id}")
async def delete_resume(resume_id: int, user: Users = Depends(get_current_user)):
    data = await ResumesDAO.find_one_or_none(id=resume_id)
    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Резюме не найдено"
        )
    try:
        result_count = await ResumesDAO.delete(id=resume_id)
    except SQLAlchemyError as e:
        msg = f"Database Exception: {e}"
        logger.error(
            msg,
            extra={"resume_id": resume_id},
            exc_info=True,
        )
        raise HTTPException(status_code=500, detail=msg)
    except Exception as e:
        msg = f"Unexpected error: {str(e)}"
        logger.error(
            msg,
            extra={"resume_id": resume_id},
            exc_info=True,
        )
        raise HTTPException(status_code=500, detail=msg)

    if result_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Резюме не найдено"
        )
    return {"status": "success", "detail": f"deleted row {result_count}"}


@router.get("/get_all_by_user")
async def get_resumes_all(user: Users = Depends(get_current_user)):
    try:
        result = await ResumesDAO.find_all(user_id=user.id)
        if result:
            return result
        raise CannotFindResume

    except SQLAlchemyError as e:
        msg = f"Database Exception{e} "
        logger.error(msg)
    except Exception as e:
        msg = f"Unexpected error: {str(e)}"
        logger.error(msg)


@router.get("/find_resume_by_id")
async def get_resume_by_id(resume_id: int, user: Users = Depends(get_current_user)):
    try:
        result = await ResumesDAO.find_one_or_none(id=resume_id)
        if result:
            return result
        raise CannotFindResume

    except SQLAlchemyError as e:
        msg = f"Database Exception  {e}"
        logger.error(
            msg,
            extra={"resume_id": resume_id},
            exc_info=True,
        )
    except Exception as e:
        msg = f"Unexpected error: {str(e)}"
        logger.error(
            msg,
            extra={"resume_id": resume_id},
            exc_info=True,
        )
