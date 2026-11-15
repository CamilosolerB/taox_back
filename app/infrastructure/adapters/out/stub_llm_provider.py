"""
Proveedor LLM de respaldo (stub) para desarrollo y pruebas sin credenciales.

Genera respuestas deterministas basadas en el último mensaje del usuario.
"""
from typing import List, Dict

from app.domain.entities.copilot_models import LlmResult
from app.domain.ports.out.llm_provider import LlmProvider


class StubLlmProvider(LlmProvider):
    """Proveedor LLM local que no requiere red ni credenciales."""

    def __init__(self, model: str = "stub-copilot"):
        self.model = model

    @property
    def name(self) -> str:
        return "stub"

    def generate(self, system_prompt: str, messages: List[Dict[str, str]]) -> LlmResult:
        last_user = ""
        for message in reversed(messages):
            if message.get("role") == "user":
                last_user = message.get("content", "")
                break

        content = (
            "Soy el copiloto de TAOX (modo de prueba, sin proveedor LLM configurado). "
            f"Recibí tu mensaje: '{last_user}'. "
            "Configura MINIMAX_API_KEY para respuestas reales."
        )
        return LlmResult(content=content, provider=self.name, model=self.model)
