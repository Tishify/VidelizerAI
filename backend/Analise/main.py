from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from uuid import uuid4
from loguru import logger
from pathlib import Path
from tinydb import TinyDB, Query
from pydantic import BaseModel
import tempfile
import shutil
import os

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

class AnalysisRequest(BaseModel):
    videoId: str
    options: dict = {}

class AnalysisResult(BaseModel):
    id: str
    videoId: str
    status: str
    progress: int = 0
    result: dict = {}
    error: str = None
    createdAt: str = None
    completedAt: str = None

# Redirect index
@app.get("/")
def root():
    logger.info("GET / → redirect to /static/index.html")
    return RedirectResponse(url="/static/index.html")

# Upload video file - соответствует frontend API
@app.post("/api/videos/upload")
def upload_video(video: UploadFile = File(...)):
    request_id = str(uuid4())
    logger.info(f"[{request_id}] 📅 Upload request from client with file: {video.filename}")

    with tempfile.NamedTemporaryFile(delete=False, suffix=Path(video.filename).suffix) as tmp:
        shutil.copyfileobj(video.file, tmp)
        temp_path = tmp.name
    logger.debug(f"[{request_id}] File saved to temp: {temp_path}")

    try:
        logger.info(f"[{request_id}] ✈️ Sending file to Whisper: http://localhost:8000/transcribe?lang=auto")
        # Заглушка відповіді Whisper
        fake_text = "[FAKE TRANSCRIPT TEXT HERE FROM WHISPER]"
        video_id = str(uuid4())
        transcripts_db.insert({"id": video_id, "text": fake_text})
        logger.success(f"[{request_id}] ✅ Received text ({len(fake_text)} chars)")
        return {"success": True, "videoId": video_id}
    finally:
        os.remove(temp_path)
        logger.debug(f"[{request_id}] 🪚 Temp file removed")

# Start video analysis - соответствует frontend API
@app.post("/api/videos/analyze")
def start_analysis(request: AnalysisRequest):
    analysis_id = str(uuid4())
    logger.info(f"Starting analysis for video {request.videoId}")
    
    # Создаем запись анализа
    analysis_result = {
        "id": analysis_id,
        "videoId": request.videoId,
        "status": "processing",
        "progress": 0,
        "result": {
            "summary": "Video analysis in progress...",
            "keyPoints": ["Point 1", "Point 2"],
            "sentiment": "neutral",
            "duration": 120,
            "language": "en"
        },
        "error": None,
        "createdAt": "2024-01-01T00:00:00Z",
        "completedAt": None
    }
    
    return analysis_result

# Get analysis status - соответствует frontend API
@app.get("/api/analysis/{analysis_id}")
def get_analysis_status(analysis_id: str):
    logger.info(f"Getting analysis status for {analysis_id}")
    
    # Возвращаем фейковый результат
    return {
        "id": analysis_id,
        "videoId": "fake-video-id",
        "status": "completed",
        "progress": 100,
        "result": {
            "summary": "This is a fake analysis result for demonstration purposes.",
            "keyPoints": ["Key point 1", "Key point 2", "Key point 3"],
            "sentiment": "positive",
            "duration": 180,
            "language": "en"
        },
        "error": None,
        "createdAt": "2024-01-01T00:00:00Z",
        "completedAt": "2024-01-01T00:05:00Z"
    }

# Get analysis results - соответствует frontend API
@app.get("/api/videos/{video_id}/analysis")
def get_analysis_results(video_id: str):
    logger.info(f"Getting analysis results for video {video_id}")
    
    # Возвращаем список результатов анализа
    return [
        {
            "id": "analysis-1",
            "videoId": video_id,
            "status": "completed",
            "progress": 100,
            "result": {
                "summary": "First analysis result",
                "keyPoints": ["Point A", "Point B"],
                "sentiment": "positive",
                "duration": 120,
                "language": "en"
            },
            "error": None,
            "createdAt": "2024-01-01T00:00:00Z",
            "completedAt": "2024-01-01T00:03:00Z"
        }
    ]

# Legacy endpoints for backward compatibility
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
