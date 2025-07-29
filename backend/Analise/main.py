from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from uuid import uuid4
from loguru import logger
from pathlib import Path
from tinydb import TinyDB, Query
from pydantic import BaseModel
import tempfile
import shutil
import os

app = FastAPI()

# Ensure db directory exists
Path("db").mkdir(parents=True, exist_ok=True)

# Static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# DB init
transcripts_db = TinyDB("db/transcripts.json")
chats_db = TinyDB("db/chats.json")

# Models
class Transcript(BaseModel):
    id: str
    text: str

class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str

class ChatHistory(BaseModel):
    transcript_id: str
    messages: list[ChatMessage]

# Redirect index
@app.get("/")
def root():
    logger.info("GET / → redirect to /static/index.html")
    return RedirectResponse(url="/static/index.html")

# Upload and transcribe
@app.post("/upload")
def upload_and_transcribe(file: UploadFile = File(...)):
    request_id = str(uuid4())
    logger.info(f"[{request_id}] 📅 Upload request from client with file: {file.filename}")

    with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix) as tmp:
        shutil.copyfileobj(file.file, tmp)
        temp_path = tmp.name
    logger.debug(f"[{request_id}] File saved to temp: {temp_path}")

    try:
        logger.info(f"[{request_id}] ✈️ Sending file to Whisper: http://localhost:8000/transcribe?lang=auto")
        # Заглушка відповіді Whisper
        fake_text = "[FAKE TRANSCRIPT TEXT HERE FROM WHISPER]"
        transcript_id = str(uuid4())
        transcripts_db.insert({"id": transcript_id, "text": fake_text})
        logger.success(f"[{request_id}] ✅ Received text ({len(fake_text)} chars)")
        return {"transcript_id": transcript_id, "text": fake_text}
    finally:
        os.remove(temp_path)
        logger.debug(f"[{request_id}] 🪚 Temp file removed")

# Get transcript
@app.get("/transcript/{transcript_id}")
def get_transcript(transcript_id: str):
    TranscriptQuery = Query()
    record = transcripts_db.get(TranscriptQuery.id == transcript_id)
    if not record:
        return JSONResponse(status_code=404, content={"error": "Transcript not found"})
    return record

# Chat: send message
@app.post("/chat/{transcript_id}")
def send_message(transcript_id: str, message: ChatMessage):
    ChatQuery = Query()
    history = chats_db.get(ChatQuery.transcript_id == transcript_id)
    if not history:
        history = {"transcript_id": transcript_id, "messages": []}

    # Додаємо нове повідомлення користувача
    history["messages"].append({"role": message.role, "content": message.content})

    # Додаємо фейкову відповідь
    assistant_reply = f"[FAKE RESPONSE to: {message.content[:30]}...]"
    history["messages"].append({"role": "assistant", "content": assistant_reply})

    # Оновлюємо БД
    chats_db.upsert(history, ChatQuery.transcript_id == transcript_id)
    return {"reply": assistant_reply}

# Chat: get full history
@app.get("/chat/{transcript_id}")
def get_chat(transcript_id: str):
    ChatQuery = Query()
    history = chats_db.get(ChatQuery.transcript_id == transcript_id)
    if not history:
        return {"messages": []}
    return history
