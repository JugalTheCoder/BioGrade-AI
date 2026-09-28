from __future__ import annotations

from transformers import pipeline


class TranslationService:
    """Lazy translation wrapper. Configure a compatible Hugging Face translation model."""

    def __init__(self, model_name: str | None = None):
        self.model_name = model_name
        self._translator = None

    def _load(self):
        if not self.model_name:
            raise ValueError("A translation model_name must be configured before translation.")
        if self._translator is None:
            self._translator = pipeline("translation", model=self.model_name)

    def translate(self, text: str) -> str:
        self._load()
        result = self._translator(text, max_length=512)
        return result[0]["translation_text"]
