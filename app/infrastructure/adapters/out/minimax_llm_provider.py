"""
Proveedor LLM MiniMax (API compatible con OpenAI)
Endpoint: POST {base_url}/chat/completions
"""
import logging
from typing import List, Dict

import requests

from app.domain.entities.copilot_models import LlmResult
from app.domain.exceptions.copilot_exceptions import LlmProviderError
from app.domain.ports.out.llm_provider import LlmProvider

logger = logging.getLogger(__name__)


class MiniMaxLlmProvider(LlmProvider):
    """Implementación del puerto LlmProvider sobre la API de MiniMax."""

    def __init__(
        self,
        api_key: str,
        model: str,
        base_url: str = "https://api.minimax.io/v1",
        max_tokens: int = 1024,
        timeout: int = 60,
    ):
        self.api_key = api_key
        self.model = model
        self.base_url = base_url.rstrip("/")
        self.max_tokens = max_tokens
        self.timeout = timeout

    @property
    def name(self) -> str:
        return "minimax"

    def generate(self, system_prompt: str, messages: List[Dict[str, str]]) -> LlmResult:
        if not self.api_key:
            raise LlmProviderError("MINIMAX_API_KEY no está configurada")

        payload = {
            "model": self.model,
            "max_tokens": self.max_tokens,
            "messages": [{"role": "system", "content": system_prompt}] + list(messages),
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                json=payload,
                headers=headers,
                timeout=self.timeout,
            )
        except requests.RequestException as exc:
            logger.error(f"Error de red al invocar MiniMax: {exc}")
            raise LlmProviderError(f"No se pudo contactar al proveedor LLM: {exc}") from exc

        if response.status_code >= 400:
            logger.error(
                f"MiniMax respondió {response.status_code}: {response.text[:500]}"
            )
            raise LlmProviderError(
                f"Proveedor LLM respondió con estado {response.status_code}"
            )

        try:
            data = response.json()
            content = data["choices"][0]["message"]["content"]
        except (ValueError, KeyError, IndexError, TypeError) as exc:
            logger.error(f"Respuesta inesperada de MiniMax: {exc}")
            raise LlmProviderError("Respuesta inválida del proveedor LLM") from exc

        if not content:
            raise LlmProviderError("El proveedor LLM devolvió una respuesta vacía")

        return LlmResult(content=content, provider=self.name, model=self.model)
