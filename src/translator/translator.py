from typing import Any, Dict, Optional

from openai import OpenAI

from src.core import get_logger
from src.core.interfaces import Translator


class GPTTranslator(Translator):
    """Переводит текст используя OpenAI модели."""

    def __init__(self, config: Dict[str, Any], model_id: Optional[str] = None):
        self.config = config
        self.client = OpenAI(api_key=config["openai"]["api_key"])
        self.model_id = model_id or config["openai"]["model"]
        self.logger = get_logger(__name__)

    def translate(self, text: str, model_id: Optional[str] = None) -> str:
        """
        Переводит текст с русского на английский.

        Args:
            text: Текст для перевода
            model_id: ID модели (если None, использует default)

        Returns:
            Переведенный текст
        """
        try:
            model = model_id or self.model_id

            self.logger.info(f"Translating text with model: {model}")

            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a professional translator. Translate the following Russian text to English, maintaining the original style and meaning.",
                    },
                    {"role": "user", "content": text},
                ],
                temperature=self.config["inference"].get("temperature", 0.3),
                max_tokens=self.config["inference"].get("max_tokens", 2000),
                top_p=self.config["inference"].get("top_p", 1.0),
            )

            translation = response.choices[0].message.content.strip()
            self.logger.info("Translation completed")

            return translation

        except Exception as e:
            self.logger.error(f"Translation error: {e}")
            raise

    def set_model(self, model_id: str) -> None:
        """Устанавливает модель для использования."""
        self.model_id = model_id
        self.logger.info(f"Model changed to: {model_id}")
