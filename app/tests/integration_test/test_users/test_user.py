import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    "email,password,status_code",
    [
        ("Ilmir11122@gmail.com", "19513q", 201),
        ("Ilmir11122@gmail.com", "1953a", 409),
        ("Ilmir112gmail.com", "1953a", 422),  # Некорректный email, ожидаем 422
    ],
)
async def test_register(email, password, status_code, ac: AsyncClient):
    response = await ac.post(
        "/auth/register",
        json={"email": email, "password": password},
    )
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "email,password,status_code",
    [("Ilmir112@gmail.com", "1953s", 200), ("Ilmir112@gmail.com", "1234563a", 200)],
)
async def test_login(email, password, status_code, ac: AsyncClient):
    response = await ac.post(
        "/auth/login",
        json={"email": email, "password": password},  # Используем 'password'
    )
    assert response.status_code == status_code

