# MVP План - Анализ звонков продажников

## 🎯 Цель MVP
Создать минимально жизнеспособный продукт для анализа звонков продажников с базовым функционалом.

## 📋 Основные функции MVP

### 1. Загрузка видео в приложение
### 2. Транскрипция аудио в текст  
### 3. Отправка в ИИ с промптом
### 4. Получение и отображение ответа

---

## 🏗️ Архитектура MVP

### Frontend (React + TypeScript)
```
src/
├── components/
│   ├── VideoUpload/          # Drag & Drop загрузка
│   ├── AnalysisResults/      # Результаты анализа
│   └── LoadingSpinner/       # Индикатор загрузки
├── pages/
│   ├── UploadPage.tsx        # Страница загрузки
│   └── ResultsPage.tsx       # Страница результатов
├── services/
│   ├── api.ts               # API клиент
│   └── fileUpload.ts        # Логика загрузки
└── types/
    └── index.ts             # TypeScript типы
```

### Backend (FastAPI + Python)
```
app/
├── main.py                  # FastAPI приложение
├── api/
│   ├── upload.py           # Эндпоинт загрузки
│   └── analysis.py         # Эндпоинт анализа
├── services/
│   ├── transcription.py    # Транскрипция
│   ├── ai_analysis.py     # Анализ ИИ
│   ├── youtube.py         # Загрузка на YouTube
│   └── search_service.py   # Поиск и фильтрация
├── models/
│   ├── analysis.py        # MongoDB модели
│   └── database.py        # MongoDB подключение
└── utils/
    └── file_handler.py    # Обработка файлов
```

### База данных (MongoDB)
```javascript
// Коллекция анализов
{
  "_id": ObjectId("..."),
  "title": "Sales Call Analysis",
  "original_filename": "call_001.mp4",
  "youtube_url": "https://youtube.com/watch?v=...",
  "transcription": {
    "text": "Полный текст транскрипции...",
    "segments": [
      {
        "start": 0,
        "end": 30,
        "text": "Привет, это Иван..."
      }
    ]
  },
  "analysis": {
    "score": 85,
    "errors": [
      {
        "type": "objection_handling",
        "description": "Не ответил на возражение...",
        "timestamp": 120
      }
    ],
    "recommendations": [
      "Используйте технику активного слушания..."
    ]
  },
  "custom_queries": [
    {
      "question": "Как улучшить технику закрытия?",
      "answer": "Рекомендую использовать...",
      "created_at": ISODate("2024-01-15")
    }
  ],
  "tags": ["cold_call", "objection_handling"],
  "metadata": {
    "duration": 300,
    "call_type": "cold_call",
    "sales_stage": "prospecting"
  },
  "status": "completed",
  "created_at": ISODate("2024-01-15T10:30:00Z"),
  "updated_at": ISODate("2024-01-15T10:35:00Z")
}

// Коллекция промптов
{
  "_id": ObjectId("..."),
  "name": "Sales Analysis Prompt",
  "content": "Проанализируй звонок продажника...",
  "category": "error_analysis",
  "is_active": true,
  "priority": 1,
  "created_at": ISODate("2024-01-15T10:30:00Z")
}
```

---

## 🍃 Преимущества MongoDB для MVP

### ✅ **Гибкость данных ИИ**
- Легко добавлять новые поля анализа
- Естественная работа с JSON структурами
- Нет необходимости в миграциях схемы

### ✅ **Мощные агрегации**
```javascript
// Статистика по типам ошибок
db.analyses.aggregate([
  { $unwind: "$analysis.errors" },
  { $group: { _id: "$analysis.errors.type", count: { $sum: 1 } }}
])

// Поиск по тегам и оценкам
db.analyses.find({
  "tags": { $in: ["cold_call"] },
  "analysis.score": { $gte: 70 }
})
```

### ✅ **Простота разработки**
- Меньше настройки схемы
- Нативная поддержка JSON
- Быстрая итерация

### ✅ **Масштабируемость**
- Горизонтальное масштабирование
- Шардинг для больших объемов
- Готовность к росту

---

## 🚀 Этапы разработки

### Этап 1: Базовая настройка (1-2 дня)
- [ ] Создать React приложение
- [ ] Настроить FastAPI backend
- [ ] Подключить MongoDB
- [ ] Настроить Docker для разработки

### Этап 2: Загрузка видео (2-3 дня)
- [ ] Создать drag & drop компонент
- [ ] Реализовать валидацию файлов (mp3, mp4)
- [ ] Настроить загрузку на сервер
- [ ] Добавить индикатор прогресса

### Этап 3: Транскрипция (2-3 дня)
- [ ] Интеграция с OpenAI Whisper API
- [ ] Обработка аудио файлов
- [ ] Сохранение транскрипции в БД
- [ ] Обработка ошибок

### Этап 4: Анализ ИИ (2-3 дня)
- [ ] Создать базовые промпты
- [ ] Интеграция с ChatGPT API
- [ ] Анализ текста транскрипции
- [ ] Сохранение результатов

### Этап 5: YouTube интеграция (1-2 дня)
- [ ] Настройка YouTube Data API
- [ ] Автоматическая загрузка видео
- [ ] Сохранение ссылок в БД

### Этап 6: UI/UX (2-3 дня)
- [ ] Создать страницу результатов
- [ ] Добавить навигацию
- [ ] Стилизация компонентов
- [ ] Адаптивный дизайн

---

## 💻 Технический стек

### Frontend
```json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-dropzone": "^14.2.3",
    "react-query": "^3.39.3",
    "axios": "^1.6.0",
    "tailwindcss": "^3.3.0"
  }
}
```

### Backend
```json
{
  "dependencies": {
    "fastapi": "^0.104.0",
    "uvicorn": "^0.24.0",
    "motor": "^3.3.2",
    "pymongo": "^4.6.0",
    "python-multipart": "^0.0.6",
    "openai": "^1.3.0",
    "google-api-python-client": "^2.108.0",
    "python-dotenv": "^1.0.0",
    "pydantic": "^2.5.0"
  }
}
```

---

## 🔧 Конфигурация

### Environment Variables
```bash
# Database
MONGODB_URL=mongodb://admin:password@localhost:27017/sales_analysis

# OpenAI
OPENAI_API_KEY=your_openai_key

# YouTube
YOUTUBE_CLIENT_ID=your_youtube_client_id
YOUTUBE_CLIENT_SECRET=your_youtube_client_secret
YOUTUBE_REFRESH_TOKEN=your_refresh_token

# App
SECRET_KEY=your_secret_key
```

### Docker Compose
```yaml
version: '3.8'
services:
  frontend:
    build: ./frontend
    ports: ["3000:3000"]
    volumes: ["./frontend:/app", "/app/node_modules"]
  
  backend:
    build: ./backend
    ports: ["8000:8000"]
    environment:
      - MONGODB_URL=mongodb://admin:password@mongodb:27017/sales_analysis
    depends_on: [mongodb]
  
  mongodb:
    image: mongo:7.0
    ports:
      - "27017:27017"
    environment:
      MONGO_INITDB_ROOT_USERNAME: admin
      MONGO_INITDB_ROOT_PASSWORD: password
    volumes:
      - mongodb_data:/data/db
      - ./mongo-init.js:/docker-entrypoint-initdb.d/mongo-init.js:ro

volumes:
  mongodb_data:
```

---

## 📝 API Endpoints

### Загрузка
```python
POST /api/upload/video
Content-Type: multipart/form-data

Response:
{
  "analysis_id": "uuid",
  "status": "processing",
  "message": "Video uploaded successfully"
}
```

### Статус обработки
```python
GET /api/analysis/{analysis_id}/status

Response:
{
  "status": "completed|processing|failed",
  "progress": 75,
  "current_step": "transcription"
}
```

### Результаты анализа
```python
GET /api/analysis/{analysis_id}

Response:
{
  "id": "object_id",
  "title": "Sales Call Analysis",
  "youtube_url": "https://youtube.com/watch?v=...",
  "transcription": {
    "text": "Полный текст транскрипции...",
    "segments": [...]
  },
  "analysis": {
    "score": 85,
    "errors": [...],
    "recommendations": [...]
  },
  "tags": ["cold_call", "objection_handling"],
  "metadata": {
    "duration": 300,
    "call_type": "cold_call"
  },
  "created_at": "2024-01-15T10:30:00Z"
}
```

---

## 🎨 UI/UX Дизайн

### Главная страница (UploadPage)
```
┌─────────────────────────────────────┐
│           Sales Call Analyzer       │
├─────────────────────────────────────┤
│                                     │
│    [Drag & Drop Video Here]         │
│                                     │
│    or click to select file          │
│                                     │
│    Supported: MP3, MP4 (max 100MB) │
│                                     │
└─────────────────────────────────────┘
```

### Страница результатов (ResultsPage)
```
┌─────────────────────────────────────┐
│  Sales Call Analysis - Results      │
├─────────────────────────────────────┤
│                                     │
│  📹 YouTube: [Watch Video]          │
│                                     │
│  📝 Transcription:                  │
│  [Full text with timestamps]        │
│                                     │
│  🔍 Analysis:                       │
│  [Detailed sales analysis]          │
│                                     │
│  📊 Score: 85/100                   │
│                                     │
└─────────────────────────────────────┘
```

---

## 🧪 Тестирование

### Unit Tests
- [ ] Тесты загрузки файлов
- [ ] Тесты транскрипции
- [ ] Тесты анализа ИИ
- [ ] Тесты YouTube интеграции

### Integration Tests
- [ ] End-to-end тест загрузки
- [ ] Тест полного процесса анализа
- [ ] Тест обработки ошибок

---

## 📊 Метрики успеха

### Технические
- [ ] Время загрузки видео < 30 сек
- [ ] Время транскрипции < 5 мин
- [ ] Время анализа ИИ < 2 мин
- [ ] Успешность загрузки на YouTube > 95%

### Пользовательские
- [ ] Простота загрузки файлов
- [ ] Понятность результатов анализа
- [ ] Скорость получения результатов
- [ ] Качество транскрипции

---

## 🚀 Деплой

### Development
```bash
# Frontend
cd frontend && npm run dev

# Backend
cd backend && uvicorn main:app --reload

# Database
docker-compose up mongodb
```

### Production
```bash
# Build and deploy
docker-compose -f docker-compose.prod.yml up -d
```

---

## 📅 Timeline

| Этап | Длительность | Результат |
|------|-------------|-----------|
| Настройка | 2 дня | Базовая инфраструктура |
| Загрузка | 3 дня | Drag & drop функционал |
| Транскрипция | 3 дня | Работающая транскрипция |
| Анализ ИИ | 3 дня | Анализ продажников |
| YouTube | 2 дня | Автозагрузка на YouTube |
| UI/UX | 3 дня | Красивый интерфейс |
| **Итого** | **16 дней** | **Готовый MVP** |

---

## 🔄 Следующие шаги после MVP

1. **Добавить фильтрацию** истории анализов (MongoDB агрегации)
2. **Реализовать кастомные промпты**
3. **Добавить экспорт в PDF**
4. **Создать админ панель**
5. **Добавить аутентификацию**
6. **Реализовать сравнение анализов**
7. **Добавить полнотекстовый поиск** (MongoDB $text)
8. **Реализовать аналитику** (MongoDB агрегации) 