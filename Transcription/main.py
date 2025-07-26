from fastapi import FastAPI, File, UploadFile, BackgroundTasks
import whisper
import shutil
import os

app = FastAPI()
model = whisper.load_model("medium")

def transcribe_audio(file_path: str, result_path: str):
    result = model.transcribe(file_path, language="Ukrainian", fp16=False)
    with open(result_path, "w", encoding="utf-8") as f:
        f.write(result["text"])
    print(f"Transcription saved to: {result_path}")

@app.post("/transcribe")
async def transcribe_endpoint(file: UploadFile = File(...), background_tasks: BackgroundTasks = BackgroundTasks()):
    temp_path = f"temp_{file.filename}"
    result_path = f"{file.filename}.txt"

    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    background_tasks.add_task(transcribe_audio, temp_path, result_path)
    return {"status": "processing", "filename": file.filename, "output": result_path}
