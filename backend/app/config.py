from __future__ import annotations

import os


APP_ENV = os.getenv("APP_ENV", os.getenv("FASTAPI_ENV", "development")).strip().lower()
IS_PRODUCTION = APP_ENV == "production"
API_VERSION = "1.1.0"


def cors_origins() -> list[str]:
    raw = os.getenv("CORS_ORIGINS", "")
    if raw.strip():
        return [item.strip() for item in raw.split(",") if item.strip()]
    if not IS_PRODUCTION:
        return ["http://localhost:3000", "http://localhost:5173", "http://localhost:8080"]
    return []


def allowed_hosts() -> list[str]:
    raw = os.getenv("ALLOWED_HOSTS", "")
    return [item.strip() for item in raw.split(",") if item.strip()] or ["*"]


def validate_production_configuration() -> None:
    if not IS_PRODUCTION:
        return

    jwt_secret = os.getenv("JWT_SECRET", "")
    if not jwt_secret or jwt_secret == "dev-only-change-before-deployment":
        raise RuntimeError("JWT_SECRET must be configured with a non-development value in production.")

    if not cors_origins():
        raise RuntimeError("CORS_ORIGINS must be explicitly configured in production.")

    if allowed_hosts() == ["*"]:
        raise RuntimeError("ALLOWED_HOSTS must be explicitly configured in production.")
