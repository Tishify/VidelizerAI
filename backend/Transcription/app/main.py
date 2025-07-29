from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import JSONResponse
from loguru import logger
import whisper
import tempfile
import os
import uuid

app = FastAPI()
model = whisper.load_model("medium")

# Логирование
logger.add("logs/whisper.log", rotation="1 MB", level="DEBUG", backtrace=True, diagnose=True)
logger.info("Whisper API initialized")

@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...), request: Request = None, lang: str = "Ukrainian"):
    request_id = str(uuid.uuid4())
    logger.info(f"[{request_id}] 📥 Received file: {file.filename} from {request.client.host}")

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
            contents = await file.read()
            tmp.write(contents)
            tmp_path = tmp.name
            logger.debug(f"[{request_id}] 💾 Saved file to temp path: {tmp_path}")

        logger.info(f"[{request_id}] 🧠 Starting transcription")
        options = {"fp16": False}
        if lang != "auto":
            options["language"] = lang
            logger.info(f"[{request_id}] 🌍 Forced language: {lang}")
        else:
            logger.info(f"[{request_id}] 🌐 Autodetect language")

        result = model.transcribe(tmp_path, **options)

        os.remove(tmp_path)
        logger.debug(f"[{request_id}] 🧹 Temp file deleted")

        response = {
            "text": result["text"]
        }

        logger.success(f"[{request_id}] ✅ Transcription done. {len(result['text'])} characters")
        return JSONResponse(content=response)

    except Exception as e:
        logger.exception(f"[{request_id}] ❌ Transcription failed")
        return JSONResponse(status_code=500, content={"error": str(e)})
