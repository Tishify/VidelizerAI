# Архитектура приложения анализа звонков продажников

## Системная архитектура

### 1. Frontend (React + TypeScript)
```
src/
├── components/
│   ├── VideoUpload/          # Drag & Drop загрузка
│   ├── AnalysisResults/      # Страница с результатами
│   ├── CustomQueries/        # Кастомные запросы
│   └── AdminPanel/          # Управление промптами
├── services/
│   ├── api.ts               # API клиент
│   ├── websocket.ts         # Real-time обновления
│   └── fileUpload.ts        # Логика загрузки файлов
└── pages/
    ├── UploadPage.tsx
    ├── AnalysisPage.tsx
    ├── CustomQueriesPage.tsx
    └── AdminPage.tsx
```

### 2. Backend (FastAPI + Python)
```
app/
├── main.py                  # FastAPI приложение
├── api/
│   ├── upload.py           # Эндпоинты загрузки
│   ├── analysis.py         # Анализ результатов
│   ├── prompts.py          # Управление промптами
│   └── youtube.py          # Интеграция с YouTube
├── services/
│   ├── transcription.py    # Транскрипция
│   ├── analysis.py         # Анализ продажника
│   ├── youtube_upload.py   # Загрузка на YouTube
│   └── database.py         # Работа с БД
├── models/
│   ├── video.py           # Модель видео
│   ├── analysis.py        # Модель анализа
│   └── prompt.py          # Модель промптов
└── utils/
    ├── file_handlers.py    # Обработка файлов
    └── validators.py       # Валидация
```

### 3. База данных (PostgreSQL)
```sql
-- Таблица видео
CREATE TABLE videos (
    id UUID PRIMARY KEY,
    filename VARCHAR(255),
    original_path VARCHAR(500),
    youtube_url VARCHAR(500),
    transcription_text TEXT,
    upload_date TIMESTAMP,
    status VARCHAR(50)
);

-- Таблица анализа
CREATE TABLE analyses (
    id UUID PRIMARY KEY,
    video_id UUID REFERENCES videos(id),
    prompt_id UUID REFERENCES prompts(id),
    analysis_result JSONB,
    custom_queries JSONB,
    created_at TIMESTAMP
);

-- Таблица промптов
CREATE TABLE prompts (
    id UUID PRIMARY KEY,
    name VARCHAR(255),
    content TEXT,
    is_active BOOLEAN,
    created_at TIMESTAMP
);
```

## Поток данных

### 1. Загрузка видео
```
User → Drag & Drop → Frontend → FastAPI → 
File Storage → TranscriptionService → 
ChatGPT API → Analysis → Database
```

### 2. Анализ продажника
```
Video Text → Prompt Selection → 
ChatGPT API → Error Analysis → 
Results Storage → Frontend Display
```

### 3. YouTube интеграция
```
Processed Video → YouTube API → 
Channel Upload → URL Storage → 
Database Update
```

## Технологический стек

### Frontend
- **React 18** + TypeScript
- **React Dropzone** для drag & drop
- **React Query** для кэширования
- **Socket.io** для real-time обновлений
- **Tailwind CSS** для стилизации

### Backend
- **FastAPI** для API
- **Celery** для фоновых задач
- **Redis** для кэша и очередей
- **PostgreSQL** для основной БД
- **MinIO/S3** для хранения файлов

### Интеграции
- **OpenAI API** для анализа
- **YouTube Data API** для загрузки
- **WebSocket** для real-time обновлений

## API Endpoints

### Загрузка
```python
POST /api/upload/video
POST /api/upload/audio
GET /api/upload/status/{id}
```

### Анализ
```python
POST /api/analysis/start
GET /api/analysis/{id}
POST /api/analysis/custom-query
```

### Промпты
```python
GET /api/prompts
POST /api/prompts
PUT /api/prompts/{id}
DELETE /api/prompts/{id}
```

### YouTube
```python
POST /api/youtube/upload
GET /api/youtube/status/{id}
```

## Безопасность

### Аутентификация
- **JWT токены** для API
- **OAuth2** для YouTube интеграции
- **API ключи** для внешних сервисов

### Валидация
- Проверка типов файлов (mp3, mp4)
- Ограничение размера файлов
- Санитизация пользовательского ввода

## Мониторинг

### Логирование
- **Structured logging** с JSON
- **Request/Response** логирование
- **Error tracking** с контекстом

### Метрики
- Время обработки файлов
- Успешность транскрипции
- Использование API лимитов

## Развертывание

### Docker Compose
```yaml
services:
  frontend:
    build: ./frontend
    ports: ["3000:3000"]
  
  backend:
    build: ./backend
    ports: ["8000:8000"]
  
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: sales_analysis
  
  redis:
    image: redis:7-alpine
  
  celery:
    build: ./backend
    command: celery -A app.celery worker
```

### CI/CD
- **GitHub Actions** для автоматического деплоя
- **Docker** для контейнеризации
- **Kubernetes** для оркестрации (опционально) 