from tinydb import TinyDB
from pathlib import Path

DB_PATH = Path(__file__).parent / "db.json"
db = TinyDB(DB_PATH)

transcriptions = db.table("transcriptions")
chats = db.table("chats")
