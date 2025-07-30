# VidelizerAI

Проект для анализа видео с использованием AI.

## Структура проекта

- `backend/Analise/` - FastAPI backend для обработки видео
- `frontend/` - React frontend приложение
- `backend/Transcription/` - Сервис транскрипции (не используется в текущей версии)

## Быстрый запуск

### Вариант 1: Автоматический запуск
```bash
./start.sh
```

### Вариант 2: Ручной запуск

#### 1. Запуск Backend
```bash
cd backend/Analise
poetry install --no-root
poetry run uvicorn main:app --host 0.0.0.0 --port 8080 --reload
```

#### 2. Запуск Frontend (в новом терминале)
```bash
cd frontend
npm install
npm start
```

## Доступные URL

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8080
- **Backend Docs**: http://localhost:8080/docs

## API Endpoints

### Backend (FastAPI)
- `POST /api/videos/upload` - Загрузка видео
- `POST /api/videos/analyze` - Начало анализа
- `GET /api/analysis/{id}` - Статус анализа
- `GET /api/videos/{id}/analysis` - Результаты анализа

### Legacy endpoints
- `POST /upload` - Старый endpoint для загрузки
- `GET /transcript/{id}` - Получение транскрипта
- `POST /chat/{id}` - Чат с AI

## Технологии

### Backend
- FastAPI
- Poetry (управление зависимостями)
- TinyDB (простая БД)
- Loguru (логирование)

### Frontend
- React 19
- TypeScript
- Tailwind CSS
- Axios (HTTP клиент)

## Разработка

### Backend разработка
```bash
cd backend/Analise
poetry shell
# Теперь можно запускать Python скрипты
```

### Frontend разработка
```bash
cd frontend
npm run build  # сборка для продакшена
npm test       # запуск тестов
```

## Примечания

- Backend использует фейковые данные для демонстрации
- CORS настроен для localhost:3000 и localhost:3001
- Все API endpoints возвращают корректные JSON ответы 