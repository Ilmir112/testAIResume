FROM python:3.11-alpine

WORKDIR /app

# Копируем только файл с зависимостями и устанавливаем их
COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Копируем весь код приложения
COPY . .

# Запускаем приложение через gunicorn с uvicorn worker
CMD ["gunicorn", "app.main:app", "--workers", "1", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:8000"]