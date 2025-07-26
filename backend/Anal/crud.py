from .models import Transcription, ChatThread
from .db import transcriptions, chats

def save_transcription(item: Transcription):
    transcriptions.insert(item.dict())

def get_transcription(id: str) -> dict | None:
    return transcriptions.get(where("id") == id)

def list_transcriptions() -> list[dict]:
    return transcriptions.all()

def save_chat(chat: ChatThread):
    chats.insert(chat.dict())

def get_chat(transcription_id: str) -> list[dict]:
    return chats.search(where("transcription_id") == transcription_id)
