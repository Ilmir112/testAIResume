from app.api.users.models import Users
from app.dao.base import BaseDAO


class UsersDAO(BaseDAO):
    model = Users
