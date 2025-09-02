FROM python:3.11-alpine

WORKDIR /app

# Копирование зависимостей и кода
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]

RUN mkdir /app

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

COPY .. .

## Эта команда также выведена в bash скрипт
  CMD ["gunicorn", "app.main:app", "--workers", "1", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:9999"]
# CMD ["gunicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
#gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:80