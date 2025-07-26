# Whisper Transcription Back-End

## Статус
Whisper успешно установлен и протестирован локально. Распознавание аудио из видеофайлов работает.

## Детали
- Модель: `medium`
- Язык: `Ukrainian`
- Пример использованного видео: 60 секунд, `.mp4`
- Формат вывода: `.txt`, `.srt`, `.vtt`

## Команда для запуска:

```bash
python -m whisper "path_to_file.mp4" --model medium --language Ukrainian --fp16 False


## Заметки
В среде Windows работает без GPU.
При использовании medium модель скачивается (~1.4 ГБ).
Поддержка ускорения возможна через CUDA (в Linux/Docker).