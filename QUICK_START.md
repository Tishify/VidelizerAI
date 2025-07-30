# 🚀 Быстрый запуск VidelizerAI

## 1. Запуск Backend
```bash
cd backend/Analise
poetry install --no-root
poetry run uvicorn main:app --host 0.0.0.0 --port 8080 --reload
```

## 2. Запуск Frontend (в новом терминале)
```bash
cd frontend
npm install
npm start
```

## 3. Проверка
- Backend: http://localhost:8080
- Frontend: http://localhost:3000
- API Docs: http://localhost:8080/docs

## 4. Тестирование
```bash
python check_status.py  # Проверка статуса
python test_api.py      # Тест API
```

## 🎯 Готово!
Откройте http://localhost:3000 в браузере и загрузите видео для анализа.

---
**Проблемы?** Смотрите `SETUP.md` для подробной инструкции. 