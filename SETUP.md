# Инструкция по запуску VidelizerAI

## Предварительные требования

1. **Python 3.10+** с Poetry
2. **Node.js 18+** с npm
3. **Git**

## Установка и запуск

### Шаг 1: Клонирование и настройка
```bash
git clone <repository-url>
cd VidelizerAI
```

### Шаг 2: Настройка Backend
```bash
cd backend/Analise
poetry install --no-root
```

### Шаг 3: Настройка Frontend
```bash
cd ../../frontend
npm install
```

### Шаг 4: Запуск

#### Вариант A: Автоматический запуск
```bash
# В корне проекта
chmod +x start.sh
./start.sh
```

#### Вариант B: Ручной запуск

**Терминал 1 - Backend:**
```bash
cd backend/Analise
poetry run uvicorn main:app --host 0.0.0.0 --port 8080 --reload
```

**Терминал 2 - Frontend:**
```bash
cd frontend
npm start
```

## Проверка работы

### Backend API
- **URL**: http://localhost:8080
- **Документация**: http://localhost:8080/docs
- **Тест API**: `python test_api.py`

### Frontend
- **URL**: http://localhost:3000
- **Автоматически откроется в браузере**

## Структура API

### Основные endpoints:
- `POST /api/videos/upload` - Загрузка видео
- `POST /api/videos/analyze` - Начало анализа
- `GET /api/analysis/{id}` - Статус анализа
- `GET /api/videos/{id}/analysis` - Результаты анализа

### Legacy endpoints:
- `POST /upload` - Старый endpoint
- `GET /transcript/{id}` - Транскрипт
- `POST /chat/{id}` - Чат

## Устранение проблем

### Backend не запускается:
1. Проверьте Python версию: `python --version`
2. Переустановите зависимости: `poetry install --no-root`
3. Проверьте порт 8080: `lsof -i :8080`

### Frontend не запускается:
1. Проверьте Node.js версию: `node --version`
2. Удалите node_modules и переустановите: `rm -rf node_modules && npm install`
3. Проверьте порт 3000: `lsof -i :3000`

### CORS ошибки:
- Backend настроен для localhost:3000 и localhost:3001
- Проверьте URL в `frontend/src/services/api.ts`

## Разработка

### Backend разработка:
```bash
cd backend/Analise
poetry shell
# Теперь можно импортировать модули проекта
```

### Frontend разработка:
```bash
cd frontend
npm run build  # сборка
npm test       # тесты
```

## Логи

- Backend логи: `backend/Analise/logs/`
- Frontend логи: в консоли браузера (F12)

## База данных

- Backend использует TinyDB (JSON файлы)
- Файлы БД: `backend/Analise/db/`
- Автоматически создаются при первом запуске 