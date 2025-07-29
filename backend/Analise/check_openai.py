import os
import requests
from loguru import logger
from dotenv import load_dotenv

# Загружаем переменные окружения из .env
load_dotenv()

try:
    import openai
except ImportError:
    logger.error("❌ Модуль `openai` не установлен. Установи его: `poetry add openai`")
    exit(1)

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    logger.error("❌ OPENAI_API_KEY не найден в .env или переменных окружения.")
    exit(1)

openai.api_key = api_key

# 🔐 Проверка подключения
logger.info("🔐 Проверка подключения к OpenAI API...")

try:
    models = openai.models.list()
    logger.success("✅ Подключение успешно. Доступные модели:")
    for m in models.data:
        logger.info(f" - {m.id}")
except Exception as e:
    logger.exception("❌ Ошибка подключения:")
    exit(1)

# 🧠 Проверка генерации ответа
logger.info("🧠 Проверка генерации текста (модель: gpt-4.1-nano)...")

try:
    response = openai.chat.completions.create(
        model="gpt-4.1-nano",
        messages=[
            {"role": "system", "content": "Ты — ассистент."},
            {"role": "user", "content": "Привет! Сколько будет 2 + 2?"}
        ]
    )
    result = response.choices[0].message.content.strip()
    logger.success(f"✅ Ответ получен: {result}")
except Exception as e:
    logger.exception("❌ Ошибка при генерации ответа:")

# 💳 Баланс (может вернуть 401 — это ожидаемо)
logger.info("💳 Проверка баланса...")

try:
    r = requests.get(
        "https://api.openai.com/v1/dashboard/billing/credit_grants",
        headers={"Authorization": f"Bearer {api_key}"}
    )
    if r.status_code == 200:
        logger.success(f"💰 Баланс: {r.json()}")
    else:
        logger.warning(f"⚠️ Статус: {r.status_code} — {r.json().get('error', {}).get('message', 'Неизвестная ошибка')}")
except Exception as e:
    logger.exception("❌ Ошибка при получении баланса:")
