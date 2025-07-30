FROM python:3.10-slim

# Установка рабочей директории
WORKDIR /app

# Копирование файлов зависимостей
COPY pyproject.toml poetry.lock ./

# Установка Poetry
RUN pip install poetry

# Настройка Poetry
RUN poetry config virtualenvs.create false

# Установка зависимостей
RUN poetry install --no-root

# Копирование исходного кода
COPY . .

# Создание директорий
RUN mkdir -p db logs static

# Открытие порта
EXPOSE 8001

# Запуск приложения
CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"] 