from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from loguru import logger
from uuid import uuid4
import tempfile
import requests
import os

from models import Transcription
from crud import save_transcription, list_transcriptions, get_transcription

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

WHISPER_API_URL = "http://localhost:8000/transcribe"


@app.get("/")
def root():
    logger.info("GET / → redirect to /static/index.html")
    return RedirectResponse(url="/static/index.html")


@app.post("/upload", summary="Upload and transcribe")
async def upload_and_process(request: Request, file: UploadFile = File(...), lang: str = "auto"):
    request_id = str(uuid4())
    logger.info(f"[{request_id}] 📥 Upload request from {request.client.host} with file: {file.filename}")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
        tmp_path = tmp.name
        content = await file.read()
        tmp.write(content)
        logger.debug(f"[{request_id}] Saved file to: {tmp_path}")

    try:
        with open(tmp_path, "rb") as f:
            logger.info(f"[{request_id}] 🚀 Sending to Whisper: {WHISPER_API_URL}?lang={lang}")
            response = requests.post(
                f"{WHISPER_API_URL}?lang={lang}",
                files={"file": (file.filename, f, file.content_type)}
            )

        if response.status_code != 200:
            logger.error(f"[{request_id}] ❌ Whisper returned {response.status_code}: {response.text}")
            return {"error": "Transcription failed", "status": response.status_code}

        result = response.json()
        transcription = Transcription(
            text=result["text"],
            video_name=file.filename,
            language=lang
        )
        save_transcription(transcription)

        logger.success(f"[{request_id}] ✅ Transcription saved: {transcription.id}")
        return {"id": transcription.id, "text": transcription.text}

    finally:
        os.remove(tmp_path)
        logger.debug(f"[{request_id}] 🧹 Temp file removed")


@app.get("/transcriptions", summary="List all transcriptions")
def list_all_transcriptions():
    return list_transcriptions()


@app.get("/transcriptions/{transcription_id}", summary="Get transcription by ID")
def get_one(transcription_id: str):
    transcription = get_transcription(transcription_id)
    if not transcription:
        return {"error": "Not found"}
    return transcription
