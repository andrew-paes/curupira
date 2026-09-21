"""Garante que o pacote `src` seja importável pelos testes."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
