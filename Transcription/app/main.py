from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from loguru import logger
import whisper
import shutil
import os
import uuid
from datetime import datetime

# ─────────────────────────────────────────────────────────────
# ИНИЦИАЛИЗАЦИЯ
# ─────────────────────────────────────────────────────────────

# Логи
os.makedirs("logs", exist_ok=True)
logger.add("logs/whisper.log", rotation="10 MB", encoding="utf-8", enqueue=True)
logger.info("🚀 Старт приложения")

# Модель
logger.info("📦 Загрузка модели Whisper...")
model = whisper.load_model("medium")
logger.info("✅ Модель загружена")

# Каталог для временных файлов
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# FastAPI instance
app = FastAPI()


# ─────────────────────────────────────────────────────────────
# Роут
# ─────────────────────────────────────────────────────────────

@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    request_id = str(uuid.uuid4())[:8]
    logger.info(f"[{request_id}] 📥 Получен файл: {file.filename}")

    try:
        # Сохраняем временный файл
        ext = os.path.splitext(file.filename)[1]
        file_path = os.path.join(UPLOAD_DIR, f"{request_id}{ext}")

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        logger.info(f"[{request_id}] 💾 Сохранён во временный файл: {file_path}")

        # Транскрибация
        logger.info(f"[{request_id}] 🧠 Старт транскрипции")
        result = model.transcribe(file_path, language="uk", fp16=False)
        text = result["text"]
        logger.success(f"[{request_id}] ✅ Готово. {len(text)} символов")

        # Удаляем файл
        os.remove(file_path)
        logger.debug(f"[{request_id}] 🧹 Временный файл удалён")

        return JSONResponse(content={"text": text})

    except Exception as e:
        logger.exception(f"[{request_id}] ❌ Ошибка: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})
