from __future__ import annotations

import hashlib
import os
import secrets
from datetime import timedelta
from uuid import uuid4

import jwt
from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerifyMismatchError, VerificationError

from app.models import UserRecord, utcnow


_password_hasher = PasswordHasher()
_DEV_JWT_SECRET = "dev-only-change-before-deployment"


class InvalidAccessTokenError(ValueError):
    pass


def _jwt_secret() -> str:
    secret = os.getenv("JWT_SECRET", _DEV_JWT_SECRET)
    if os.getenv("APP_ENV", "development").lower() == "production" and secret == _DEV_JWT_SECRET:
        raise RuntimeError("JWT_SECRET must be configured in production.")
    return secret


def access_token_seconds() -> int:
    return int(os.getenv("ACCESS_TOKEN_MINUTES", "15")) * 60


def refresh_token_days() -> int:
    return int(os.getenv("REFRESH_TOKEN_DAYS", "7"))


def hash_password(password: str) -> str:
    return _password_hasher.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    try:
        return _password_hasher.verify(password_hash, password)
    except (VerifyMismatchError, VerificationError, InvalidHashError):
        return False


def create_access_token(user: UserRecord) -> str:
    now = utcnow()
    payload = {
        "sub": str(user.id),
        "type": "access",
        "role": user.role,
        "verified": user.is_verified,
        "iat": now,
        "exp": now + timedelta(seconds=access_token_seconds()),
        "jti": str(uuid4()),
    }
    return jwt.encode(payload, _jwt_secret(), algorithm="HS256")


def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, _jwt_secret(), algorithms=["HS256"])
    except jwt.PyJWTError as exc:
        raise InvalidAccessTokenError("Invalid or expired access token.") from exc

    if payload.get("type") != "access" or not payload.get("sub"):
        raise InvalidAccessTokenError("Invalid access token.")
    return payload


def generate_refresh_token() -> str:
    return secrets.token_urlsafe(48)


def hash_refresh_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()
