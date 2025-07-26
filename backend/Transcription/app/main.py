from fastapi import FastAPI, UploadFile, File, BackgroundTasks, Query
from fastapi.responses import JSONResponse
from loguru import logger
import whisper
import shutil
import os
import uuid
import threading

# ───────────────────────────────────────────────
# ИНИЦИАЛИЗАЦИЯ
# ───────────────────────────────────────────────

# Папки
os.makedirs("logs", exist_ok=True)
os.makedirs("uploads", exist_ok=True)

# Логи
logger.add("logs/whisper.log", rotation="10 MB", encoding="utf-8", enqueue=True)
logger.info("🚀 Приложение запущено")

# Модель
logger.info("📦 Загрузка модели Whisper (medium)...")
model = whisper.load_model("medium")
logger.info("✅ Модель загружена")

# Лок на обработку
processing_lock = threading.Lock()
last_result = {"status": None, "text": None, "language": None}


# ───────────────────────────────────────────────
# ОБРАБОТКА
# ───────────────────────────────────────────────

def process_file(request_id: str, file_path: str, lang: str):
    logger.info(f"[{request_id}] 🧠 Начало транскрипции")

    try:
        # Определение языка
        options = {"fp16": False}
        if lang != "auto":
            options["language"] = lang
            logger.info(f"[{request_id}] 🌐 Язык передан: {lang}")
        else:
            options["language"] = None
            logger.info(f"[{request_id}] 🌐 Автоопределение языка")

        result = model.transcribe(file_path, **options)
        text = result["text"]
        detected_lang = result.get("language")

        # Сохраняем результат
        last_result.update({
            "status": "completed",
            "text": text,
            "language": f"{lang} (detected: {detected_lang})" if lang == "auto" else lang
        })

        logger.success(f"[{request_id}] ✅ Готово. {len(text)} символов")

    except Exception as e:
        logger.exception(f"[{request_id}] ❌ Ошибка при транскрипции: {e}")
        last_result.update({"status": "error", "text": None, "language": None})

    finally:
        os.remove(file_path)
        logger.debug(f"[{request_id}] 🧹 Временный файл удалён")
        processing_lock.release()


# ───────────────────────────────────────────────
# FASTAPI
# ───────────────────────────────────────────────

app = FastAPI()


@app.post("/transcribe")
async def transcribe(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    lang: str = Query(default="auto", description="Язык, например 'uk', 'en', 'ru' или 'auto'")
):
    request_id = str(uuid.uuid4())[:8]

    if processing_lock.locked():
        logger.warning(f"[{request_id}] 🚫 Отказ — уже идёт обработка")
        return JSONResponse(status_code=429, content={
            "status": "busy",
            "message": "Already processing another file"
        })

    try:
        processing_lock.acquire()
        ext = os.path.splitext(file.filename)[1]
        temp_path = os.path.join("uploads", f"{request_id}{ext}")

        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        logger.info(f"[{request_id}] 📥 Получен файл: {file.filename}")
        logger.info(f"[{request_id}] 💾 Сохранён как: {temp_path}")

        last_result.update({"status": "processing", "text": None, "language": None})
        background_tasks.add_task(process_file, request_id, temp_path, lang)

        return JSONResponse(status_code=202, content={
            "status": "processing",
            "message": "Transcription started",
            "request_id": request_id
        })

    except Exception as e:
        logger.exception(f"[{request_id}] ❌ Ошибка: {e}")
        if processing_lock.locked():
            processing_lock.release()
        return JSONResponse(status_code=500, content={
            "status": "error",
            "message": str(e)
        })


@app.get("/status")
async def status():
    return last_result


@app.get("/health")
async def health():
    return {"status": "ok", "message": "API is alive"}
