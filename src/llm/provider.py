"""Cliente LLM agnóstico de provedor, construído sobre LiteLLM."""
from __future__ import annotations

from dataclasses import dataclass

import litellm


class LLMError(Exception):
    """Representa uma falha da API da LLM com um tipo distinto, amigável ao usuário."""

    def __init__(self, kind: str, message: str, raw: str = ""):
        super().__init__(message)
        self.kind = kind
        self.message = message
        self.raw = raw


@dataclass
class LLMConfig:
    provider: str
    api_key: str
    endpoint: str
    model: str


class LLMClient:
    """Envolve LiteLLM para chamadas de conclusão com provedor configurável."""

    def __init__(self, config: LLMConfig):
        self.config = config

    def complete(self, prompt: str) -> str:
        """Chama a LLM e devolve o texto da resposta; levanta LLMError em falhas."""
        try:
            response = litellm.completion(
                model=f"{self.config.provider}/{self.config.model}",
                messages=[{"role": "user", "content": prompt}],
                api_key=self.config.api_key,
                api_base=self.config.endpoint,
            )
        except Exception as exc:  # noqa: BLE001 - traduzido para LLMError distinto
            raise self._translate(exc) from exc

        content = ""
        if response and getattr(response, "choices", None):
            content = (response.choices[0].message.content or "").strip()
        if not content:
            raise LLMError("incomplete", "O modelo retornou uma resposta vazia.", str(response))
        return content

    def _translate(self, exc: Exception) -> LLMError:
        msg = str(exc).lower()
        if any(k in msg for k in ("api key", "apikey", "unauthorized", "401", "invalid api")):
            return LLMError("invalid_key", "A chave de API foi rejeitada.", str(exc))
        if any(k in msg for k in ("rate limit", "429", "quota", "too many")):
            return LLMError("rate_limit", "Limite de uso excedido.", str(exc))
        if any(k in msg for k in ("timeout", "connection", "unavailable", "503", "refused")):
            return LLMError("unavailable", "O serviço da LLM está indisponível.", str(exc))
        return LLMError("error", "Erro ao chamar a LLM.", str(exc))
