from pydantic import BaseModel, Field
from typing import List, Literal
from uuid import uuid4
from datetime import datetime

class Transcription(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    text: str
    video_name: str
    language: str = "auto"
    created_at: datetime = Field(default_factory=datetime.utcnow)

class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str

class ChatThread(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    transcription_id: str
    messages: List[ChatMessage]
    created_at: datetime = Field(default_factory=datetime.utcnow)
