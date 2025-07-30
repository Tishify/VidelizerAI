FROM python:3.10-slim

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Установка рабочей директории
WORKDIR /app

# Копирование файлов зависимостей
COPY app/pyproject.toml app/poetry.lock ./

# Установка Poetry
RUN pip install poetry

# Настройка Poetry
RUN poetry config virtualenvs.create false

# Установка зависимостей
RUN poetry install --no-root

# Копирование исходного кода
COPY app/ .

# Создание директории для логов
RUN mkdir -p logs

# Открытие порта
EXPOSE 8080

# Запуск приложения
CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"] 