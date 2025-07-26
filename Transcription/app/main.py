from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "Videlizer AI Whisper API is running"}