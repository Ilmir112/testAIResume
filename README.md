# Проект: Улучшение резюме с помощью искусственного интеллекта
Данный проект — это веб-приложение для автоматического улучшения и анализа резюме с помощью ИИ. В основе лежит FastAPI для API, React для фронтенда, SQLAlchemy и Alembic для работы с базой данных, а также Docker для удобного запуска.

# Стек технологий:
-Backend: FastAPI
-Frontend: React
-ORM: SQLAlchemy
-Миграции: Alembic
-База данных: PostgreSQL
-Контейнеризация: Docker
-Основные компоненты:
API для работы с резюме: CRUD операции для добавления, редактирования, просмотра и удаления резюме.
Интерфейс пользователя (React): форма для загрузки резюме, просмотр улучшенного варианта, история.
Обработка ИИ: интеграция с моделью или API для улучшения текста резюме.
Docker: контейнеризация для быстрого запуска проекта.
# Как запустить проект
#1. Настройка окружения
Создайте файл .env в корне проекта и укажите параметры подключения к базе данных и секретные ключи:

env

# .env
MODE=DEV
LOG_LEVEL=INFO

DB_USER=login
DB_PASSWORD=password
DB_HOST=host
DB_PORT=port
DB_NAME=data_name

TEST_DB_USER=login
TEST_DB_PASSWORD=password
TEST_DB_HOST=host
TEST_DB_PORT=port
TEST_DB_NAME=data_name

OPENAI_API_KEY=API_KEY
OPENAI_BASE_URL=URL


HAWK_DSN=hawk_key
SECRET_KEY=secret_key
ALGORITHM=''
№ 2. Установка зависимостей
bash

pip install -r requirements.txt
# 3. Выполнение миграций Alembic
bash

alembic upgrade head
#4. Запуск backend (FastAPI)
bash

uvicorn app.main:app --reload
или через Docker:

bash

docker-compose up -d backend
# 5. Запуск frontend (React)
Перейдите в папку frontend и установите зависимости:

bash

cd frontend
npm install
Запустите React-приложение:

bash

npm run dev
или через Docker:

bash

docker-compose up -d frontend
# Запуск с помощью Docker
Для удобства можно использовать docker-compose. В корне проекта есть файл docker-compose.yml, который запускает все компоненты.

bash

docker-compose up -d
Это запустит:

Backend API
Frontend React
PostgreSQL
Использование
Откройте интерфейс React по адресу: http://localhost:3000
Добавляйте резюме, получайте улучшенные версии
