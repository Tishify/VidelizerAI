FROM python:3.10-slim

# Установка зависимостей
RUN apt-get update && \
    apt-get install -y ffmpeg git && \
    apt-get clean

# Создание рабочей директории
WORKDIR /app

# Копируем зависимости и код
COPY app/requirements.txt .

# Установка зависимостей проекта
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Копируем приложение
COPY app .

# Открываем порт
EXPOSE 8000

# Команда запуска
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
