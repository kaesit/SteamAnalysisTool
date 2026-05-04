"""Yerel ortam değişkenlerini yükler: yalnızca `backend/.env`.

Gerçek Client ID / Secret buraya yazılır. `.env.example` sadece şablondur,
uygulama çalışırken okunmaz (Git’e güvenle commit edilebilir).
"""

from __future__ import annotations

from pathlib import Path


def load_backend_env() -> None:
    """`backend/.env` dosyasını varsa yükler."""
    try:
        from dotenv import load_dotenv
    except ImportError:
        return

    base = Path(__file__).resolve().parent
    load_dotenv(base / ".env")
