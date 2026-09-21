"""Configuração do serviço Curupira."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


class ConfigError(Exception):
    """Levantada quando a configuração é inválida ou incompleta."""


@dataclass
class Config:
    provider: str
    api_key: str
    endpoint: str
    model: str
    directory: str

    @property
    def directory_path(self) -> Path:
        return Path(self.directory).expanduser().resolve()

    def validate(self) -> None:
        """Valida a configuração; levanta ConfigError com mensagem clara."""
        missing = []
        if not self.provider:
            missing.append("provider")
        if not self.api_key:
            missing.append("api_key")
        if not self.endpoint:
            missing.append("endpoint")
        if not self.model:
            missing.append("model")
        if not self.directory:
            missing.append("directory")
        if missing:
            raise ConfigError(f"configuração ausente: {', '.join(missing)}")
        path = self.directory_path
        if not path.exists():
            raise ConfigError(f"diretório não existe: {path}")
        if not path.is_dir():
            raise ConfigError(f"caminho não é um diretório: {path}")
