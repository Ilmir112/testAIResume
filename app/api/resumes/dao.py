import requests
from fastapi import Depends

from app.api.resumes.models import Resumes, ResumesHistory
from app.api.users.dependencies import get_current_user
from app.api.users.models import Users
from app.config import settings
from app.dao.base import BaseDAO


class ResumesHistoryDAO(BaseDAO):
    model = ResumesHistory


class ResumesDAO(BaseDAO):
    model = Resumes

    @classmethod
    async def call_ai_for_improvement(
        cls, content: str, user: Users = Depends(get_current_user)
    ) -> str:
            return content + " [Improved]"

