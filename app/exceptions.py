from fastapi import HTTPException, status


class ResumeException(HTTPException):
    status_code = 500
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserAlreadyExistsException(ResumeException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Пользователь уже существует"


class ResumeStatusExistsException(ResumeException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Резюме на найдено"


class IncorectLoginOrPassword(ResumeException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверная логин или пароль"


class TokenExpiredException(ResumeException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Срок действия токена истек"


class CannotAddDataToDatabase(ResumeException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "Не добавлено в базу данных"


class TokenAbsentException(ResumeException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Токен отсутствует"


class IncorrectTokenFormatException(ResumeException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверный формат токена"


class UserIsNotPresentException(ResumeException):
    status_code = status.HTTP_401_UNAUTHORIZED


class CannotFindResume(ResumeException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Пользователь не добавлен"
