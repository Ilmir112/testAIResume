import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    "title,context,status_code",
    [
        ("ilmir112", "1_Сезонная замена", 200),
        ("ilmir112", "1_Сезонная замена2", 200),
        ("ilmir11212", "1_Сезонная замена23у1", 200),
        ("ilmir112у3", "1_Сезонная замена12", 200),
    ],
)
async def test_add_resume(
    title,
    context,
    status_code,
    authenticated_ac: AsyncClient,
):
    response = await authenticated_ac.post(
        "/resume/add_data",
        json={"title": title, "context": context},
    )
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "resume_id, title, context, status_code",
    [
        (1, "Обновленный заголовок", "Обновленный контекст", 200),
        (9999, "Заголовок", "Контекст", 404),
    ],
)
async def test_update_resume(
    resume_id,
    title,
    context,
    status_code,
    authenticated_ac: AsyncClient,
):
    response = await authenticated_ac.put(
        f"/resume/update/{resume_id}",
        json={
            "title": title,
            "context": context,
        },
    )
    assert response.status_code == status_code
    if status_code == 200:
        # Можно дополнительно проверить содержимое ответа
        data = response.json()
        print(f"данныа {data}")


@pytest.mark.parametrize(
    "resume_id, status_code",
    [
        (1, 200),
        (9999, 404),
    ],
)
async def test_delete_resume(
    resume_id,
    status_code,
    authenticated_ac: AsyncClient,
):
    response = await authenticated_ac.delete(f"/resume/delete/{resume_id}")
    assert response.status_code == status_code
