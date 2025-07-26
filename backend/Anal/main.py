from fastapi import FastAPI, UploadFile, File, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from loguru import logger
import requests
import tempfile
import os
import uuid

app = FastAPI()

# Логирование
logger.add("logs/backend.log", rotation="1 MB", level="DEBUG", backtrace=True, diagnose=True)
logger.info("Backend API initialized")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение статики
app.mount("/static", StaticFiles(directory="static"), name="static")

WHISPER_API_URL = "http://localhost:8000/transcribe?lang=auto"

@app.get("/")
async def root():
    logger.info("GET / → redirect to /static/index.html")
    return RedirectResponse(url="/static/index.html")

@app.post("/upload")
async def upload_and_transcribe(file: UploadFile = File(...), request: Request = None):
    request_id = str(uuid.uuid4())
    logger.info(f"[{request_id}] 📥 Upload request from {request.client.host} with file: {file.filename}")

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
            contents = await file.read()
            tmp.write(contents)
            tmp_path = tmp.name
            logger.debug(f"[{request_id}] Saved file to: {tmp_path}")

        logger.info(f"[{request_id}] 🚀 Sending to Whisper: {WHISPER_API_URL}")
        with open(tmp_path, "rb") as f:
            response = requests.post(
                WHISPER_API_URL,
                files={"file": (file.filename, f, file.content_type)}
            )

        os.remove(tmp_path)
        logger.debug(f"[{request_id}] 🧹 Temp file removed")

        logger.info(f"[{request_id}] ✅ Whisper returned {response.status_code}")
        return JSONResponse(content=response.json(), status_code=response.status_code)

    except Exception as e:
        logger.exception(f"[{request_id}] ❌ Failed to process upload")
        return JSONResponse(status_code=500, content={"error": str(e)})
