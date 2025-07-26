import whisper
import sys
import os

def transcribe_video(file_path, model_name="medium", lang="Ukrainian"):
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return

    print(f"📥 Loading model '{model_name}'...")
    model = whisper.load_model(model_name)

    print(f"🎧 Transcribing '{file_path}'...")
    result = model.transcribe(file_path, language=lang, fp16=False)

    base = os.path.splitext(file_path)[0]
    txt_path = f"{base}.txt"

    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(result["text"])

    print(f"✅ Transcription saved to: {txt_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python transcribe.py path_to_video.mp4")
    else:
        transcribe_video(sys.argv[1])
