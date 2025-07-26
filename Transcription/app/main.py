from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "Videlizer AI Whisper API is running"}



# from fastapi import FastAPI, UploadFile, File
# from fastapi.responses import JSONResponse
# import whisper
# import shutil
# import uuid
# import os

# app = FastAPI()

# # Загружаем модель один раз при старте
# model = whisper.load_model("medium")

# UPLOAD_DIR = "temp_uploads"
# os.makedirs(UPLOAD_DIR, exist_ok=True)

# @app.post("/transcribe")
# async def transcribe(file: UploadFile = File(...)):
#     try:
#         # Генерируем уникальное имя
#         file_id = str(uuid.uuid4())
#         file_path = os.path.join(UPLOAD_DIR, f"{file_id}_{file.filename}")

#         # Сохраняем файл
#         with open(file_path, "wb") as buffer:
#             shutil.copyfileobj(file.file, buffer)

#         # Транскрибируем
#         result = mod
