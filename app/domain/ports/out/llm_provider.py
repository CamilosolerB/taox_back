"""
Puerto de proveedor LLM (agnóstico del proveedor concreto)
"""
from abc import ABC, abstractmethod
from typing import List, Dict

from app.domain.entities.copilot_models import LlmResult


class LlmProvider(ABC):
    """Interfaz para proveedores de lenguaje (MiniMax, stub, etc.)."""

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def generate(self, system_prompt: str, messages: List[Dict[str, str]]) -> LlmResult:
        """
        Genera una respuesta a partir del prompt de sistema y el historial.

        Args:
            system_prompt: instrucciones de sistema.
            messages: lista de dicts {"role": "user"|"assistant", "content": str}.

        Returns:
            LlmResult con el contenido generado y metadatos.

        Raises:
            LlmProviderError: si el proveedor falla.
        """
        pass
