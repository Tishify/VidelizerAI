# gpt_structurer.py

import os
from dotenv import load_dotenv
import openai
from loguru import logger

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def structure_conversation(text: str) -> str:
    logger.info("🧠 Отправка текста в OpenAI для структурирования")

    prompt = (
        "Вот расшифрованный текст разговора двух человек.\n"
        "Пожалуйста, структурируй его, добавив пометки, кто говорит. "
        "Если имена неизвестны, используй [Говорящий 1] и [Говорящий 2].\n\n"
        f"{text}"
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Или gpt-3.5-turbo
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )

        structured_text = response.choices[0].message.content.strip()
        logger.success("✅ Ответ от OpenAI получен")
        return structured_text

    except Exception as e:
        logger.exception("❌ Ошибка при обращении к OpenAI")
        return "Ошибка при структурировании текста."
