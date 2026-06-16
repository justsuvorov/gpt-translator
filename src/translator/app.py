from typing import Any, Dict

import pyedifice as e

from src.core import get_logger


class TranslatorApp:
    """PyEdifice приложение для переводчика."""

    def __init__(self, translator, config: Dict[str, Any]):
        self.translator = translator
        self.config = config
        self.logger = get_logger(__name__)

    def run(self) -> None:
        """Запускает приложение."""
        self.logger.info("Starting Translator App")

        app = e.Application("GPT Translator")

        state = {
            "is_loading": False,
        }

        with app.page():
            with e.div(style="padding: 20px; font-family: system-ui, -apple-system, sans-serif;"):
                e.h1("GPT Translator", style="color: #333; margin: 0 0 20px 0;")

                with e.div(style="display: flex; gap: 20px; height: calc(100vh - 100px);"):
                    # Левая колонна: русский текст
                    with e.div(style="flex: 1; display: flex; flex-direction: column; gap: 10px;"):
                        e.label("Russian text:", style="font-size: 12px; color: #666; font-weight: 500;")

                        russian_input = e.textarea(
                            placeholder="Enter text in Russian...",
                            style="flex: 1; padding: 10px; border: 1px solid #ddd; border-radius: 4px; font-size: 12px; font-family: monospace; resize: none;",
                        )

                        # Кнопки
                        with e.div(style="display: flex; gap: 10px;"):

                            def on_translate(_):
                                if not russian_input.value.strip():
                                    status_div.text = "Please enter Russian text"
                                    status_div.update_attr("class", "status-error")
                                    return

                                if state["is_loading"]:
                                    return

                                state["is_loading"] = True
                                status_div.text = "Translating..."
                                status_div.update_attr("class", "status-loading")

                                try:
                                    english_text = self.translator.translate(russian_input.value)
                                    english_output.value = english_text
                                    status_div.text = "Translation completed ✓"
                                    status_div.update_attr("class", "status-success")
                                except Exception as ex:
                                    self.logger.error(f"Translation error: {ex}")
                                    status_div.text = f"Error: {str(ex)}"
                                    status_div.update_attr("class", "status-error")
                                finally:
                                    state["is_loading"] = False

                            def on_clear(_):
                                russian_input.value = ""
                                english_output.value = ""
                                status_div.text = ""
                                status_div.update_attr("class", "")

                            e.button(
                                "Translate",
                                on_click=on_translate,
                                style="flex: 1; padding: 10px 20px; font-size: 12px; background: #4CAF50; color: white; border: none; border-radius: 4px; cursor: pointer; font-weight: 500;",
                            )

                            e.button(
                                "Clear",
                                on_click=on_clear,
                                style="flex: 1; padding: 10px 20px; font-size: 12px; background: #666; color: white; border: none; border-radius: 4px; cursor: pointer; font-weight: 500;",
                            )

                        status_div = e.div(
                            "",
                            style="padding: 10px; font-size: 11px; min-height: 20px; border-radius: 4px; background: #f5f5f5;",
                        )

                    # Правая колонна: английский перевод
                    with e.div(style="flex: 1; display: flex; flex-direction: column; gap: 10px;"):
                        e.label("English translation:", style="font-size: 12px; color: #666; font-weight: 500;")

                        english_output = e.textarea(
                            placeholder="Translation will appear here...",
                            readonly=True,
                            style="flex: 1; padding: 10px; border: 1px solid #ddd; border-radius: 4px; font-size: 12px; font-family: monospace; resize: none;",
                        )

            e.style(
                """
                .status-success {
                    background: #e8f5e9 !important;
                    color: #2e7d32 !important;
                }
                .status-error {
                    background: #ffebee !important;
                    color: #c62828 !important;
                }
                .status-loading {
                    background: #e3f2fd !important;
                    color: #1565c0 !important;
                }
                """
            )

        app.run()
