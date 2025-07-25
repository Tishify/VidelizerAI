# Анализ очередей для сервиса транскрипции

## Проблема: Обработка множественных запросов

### Текущая ситуация:
- TranscriptionService может обрабатывать только 1 запрос за раз
- Нужно обрабатывать множество видео одновременно
- Требуется надежная доставка сообщений

## Решения для масштабирования

### 1. **Redis + Celery (Рекомендуемое)**

**Преимущества:**
- Простая настройка
- Встроенная поддержка в FastAPI
- Автоматические retry механизмы
- Мониторинг через Flower

**Архитектура:**
```
FastAPI → Redis → Celery Workers → TranscriptionService
```

**Пример реализации:**
```python
# tasks.py
from celery import Celery
from app.services.transcription import transcribe_video

celery = Celery('transcription')

@celery.task(bind=True, max_retries=3)
def transcribe_video_task(self, video_id: str):
    try:
        result = transcribe_video(video_id)
        return result
    except Exception as exc:
        self.retry(countdown=60, exc=exc)

# api/upload.py
@router.post("/upload")
async def upload_video(file: UploadFile):
    video_id = save_video(file)
    # Асинхронная обработка
    transcribe_video_task.delay(video_id)
    return {"video_id": video_id, "status": "processing"}
```

### **Redis + Celery** - оптимальное решение

**Почему:**
1. **Простота**: Легко настроить и поддерживать
2. **Производительность**: Достаточно для 100+ одновременных транскрипций
3. **Надежность**: Встроенные retry механизмы
4. **Мониторинг**: Flower для отслеживания задач

### Архитектура с Redis:

```
┌─────────────┐    ┌─────────┐    ┌─────────────────┐
│   Frontend  │───▶│ FastAPI │───▶│   Redis Queue   │
└─────────────┘    └─────────┘    └─────────────────┘
                           │              │
                           ▼              ▼
                    ┌─────────────┐    ┌─────────────────┐
                    │   Database  │    │  Celery Workers │
                    └─────────────┘    └─────────────────┘
                                              │
                                              ▼
                                    ┌─────────────────┐
                                    │TranscriptionSvc │
                                    └─────────────────┘
```

### Конфигурация:

```python
# celery_config.py
from celery import Celery

celery_app = Celery(
    'transcription_app',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/1',
    include=['app.tasks.transcription']
)

celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 минут на транскрипцию
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
)
```

### Docker Compose с Redis:

```yaml
version: '3.8'
services:
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  celery_worker:
    build: ./backend
    command: celery -A app.celery worker --loglevel=info --concurrency=4
    depends_on:
      - redis
      - postgres
    environment:
      - CELERY_BROKER_URL=redis://redis:6379/0
      - CELERY_RESULT_BACKEND=redis://redis:6379/1

  celery_flower:
    build: ./backend
    command: celery -A app.celery flower
    ports:
      - "5555:5555"
    depends_on:
      - redis
    environment:
      - CELERY_BROKER_URL=redis://redis:6379/0

volumes:
  redis_data:
```

## Когда переходить на RabbitMQ?

### Переходите на RabbitMQ если:

1. **Высокая нагрузка**: >500 одновременных транскрипций
2. **Сложная маршрутизация**: Разные типы обработки
3. **Гарантированная доставка**: Критично для бизнеса
4. **Микросервисы**: Много независимых сервисов

### Пример с RabbitMQ:

```python
# celery_config.py
celery_app = Celery(
    'transcription_app',
    broker='amqp://guest:guest@localhost:5672//',
    backend='rpc://',
    include=['app.tasks.transcription']
)

# tasks.py
@celery_app.task(queue='transcription', routing_key='transcription.high')
def transcribe_video_high_priority(video_id: str):
    # Высокий приоритет
    pass

@celery_app.task(queue='transcription', routing_key='transcription.low')
def transcribe_video_low_priority(video_id: str):
    # Низкий приоритет
    pass
```

## Мониторинг и метрики

### Redis + Celery:
- **Flower**: Веб-интерфейс для мониторинга
- **Redis Commander**: Управление Redis
- **Prometheus**: Метрики производительности

### RabbitMQ:
- **Management UI**: Встроенный веб-интерфейс
- **Prometheus**: Экспорт метрик
- **Grafana**: Дашборды

## Вывод

**Для вашего проекта используйте Redis + Celery** потому что:

1. ✅ Простота настройки и поддержки
2. ✅ Достаточная производительность
3. ✅ Встроенные retry механизмы
4. ✅ Хороший мониторинг
5. ✅ Меньше ресурсов
