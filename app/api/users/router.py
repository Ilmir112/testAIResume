from fastapi import APIRouter, Depends, Response

from app.api.users.auth import authenticate_user, create_access_token, get_password_hash
from app.api.users.dao import UsersDAO
from app.api.users.dependencies import get_current_user
from app.api.users.models import Users
from app.api.users.schemas import SUserAuth
from app.exceptions import (
    CannotAddDataToDatabase,
    IncorectLoginOrPassword,
    UserAlreadyExistsException,
)
from app.logger import logger

router = APIRouter(
    prefix="/api/auth",
    tags=["Auth"],
)

@router.post("/login")
async def login_user(response: Response, user_data: SUserAuth):
    user = await authenticate_user(user_data.email, user_data.password)
    if user:
        access_token = create_access_token({"sub": str(user.id)})
        response.set_cookie("access_token", access_token, httponly=True)
        return {"access_token": access_token}
    return IncorectLoginOrPassword


@router.post("/register", status_code=201)
async def register_user(user_data: SUserAuth):
    existing_user = await UsersDAO.find_one_or_none(email=user_data.email)
    if existing_user:
        raise UserAlreadyExistsException
    hashed_password = get_password_hash(user_data.password)
    new_user = await UsersDAO.add(
        email=user_data.email, hashed_password=hashed_password
    )
    if not new_user:
        raise CannotAddDataToDatabase





@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("access_token")


@router.get("/me")
async def read_users_me(current_user: Users = Depends(get_current_user)):
    return current_user


@router.delete("/delete")
async def delete_user(current_user: Users = Depends(get_current_user)):
    try:
        result = await UsersDAO.delete(id=current_user.id)
        return result
    except Exception as e:
        logger.error(e)
