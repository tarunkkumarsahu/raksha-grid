from __future__ import annotations

import hmac
import os
from datetime import timedelta, timezone

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models import RefreshTokenRecord, UserRecord, utcnow

from .schemas import LoginRequest, RegisterRequest, TokenPair, UserRead
from .security import (
    access_token_seconds,
    create_access_token,
    generate_refresh_token,
    hash_password,
    hash_refresh_token,
    refresh_token_days,
    verify_password,
)


class AuthConflictError(ValueError):
    pass


class AuthCredentialsError(ValueError):
    pass


class AuthTokenError(ValueError):
    pass


def _normalize_email(email: str) -> str:
    return email.strip().lower()


def _user_read(user: UserRecord) -> UserRead:
    return UserRead(
        id=user.id,
        email=user.email,
        display_name=user.display_name,
        role=user.role,
        is_active=user.is_active,
        is_verified=user.is_verified,
        created_at=user.created_at,
    )


def _response_team_verified(code: str | None) -> bool:
    expected = os.getenv("RESPONSE_TEAM_REGISTRATION_CODE")
    return bool(expected and code and hmac.compare_digest(expected, code))


def register_user(session: Session, payload: RegisterRequest) -> UserRead:
    email = _normalize_email(str(payload.email))
    existing = session.scalar(select(UserRecord).where(UserRecord.email == email))
    if existing is not None:
        raise AuthConflictError("An account with this email already exists.")

    role_verified = (
        True
        if payload.role == "citizen"
        else _response_team_verified(payload.response_team_verification_code)
    )
    if payload.role == "response_team" and os.getenv("APP_ENV", "development").lower() == "production" and not role_verified:
        raise AuthConflictError(
            "Response Team self-registration requires an approved verification code in production."
        )
    user = UserRecord(
        email=email,
        display_name=payload.display_name.strip(),
        password_hash=hash_password(payload.password),
        role=payload.role,
        is_active=True,
        is_verified=role_verified,
    )
    session.add(user)
    try:
        session.commit()
    except IntegrityError as exc:
        session.rollback()
        raise AuthConflictError("An account with this email already exists.") from exc
    return _user_read(user)


def authenticate_user(session: Session, payload: LoginRequest) -> UserRecord:
    email = _normalize_email(str(payload.email))
    user = session.scalar(select(UserRecord).where(UserRecord.email == email))
    if user is None or not verify_password(payload.password, user.password_hash):
        raise AuthCredentialsError("Invalid email or password.")
    if not user.is_active:
        raise AuthCredentialsError("Account is inactive.")
    return user


def _issue_token_pair(session: Session, user: UserRecord) -> TokenPair:
    access_token = create_access_token(user)
    refresh_token = generate_refresh_token()
    session.add(
        RefreshTokenRecord(
            user_id=user.id,
            token_hash=hash_refresh_token(refresh_token),
            expires_at=utcnow() + timedelta(days=refresh_token_days()),
        )
    )
    session.commit()
    return TokenPair(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=access_token_seconds(),
        user=_user_read(user),
    )


def login_user(session: Session, payload: LoginRequest) -> TokenPair:
    return _issue_token_pair(session, authenticate_user(session, payload))


def _as_aware(value):
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value


def refresh_tokens(session: Session, raw_refresh_token: str) -> TokenPair:
    token_hash = hash_refresh_token(raw_refresh_token)
    record = session.scalar(
        select(RefreshTokenRecord).where(RefreshTokenRecord.token_hash == token_hash)
    )
    if record is None or record.revoked_at is not None:
        raise AuthTokenError("Invalid refresh token.")
    if _as_aware(record.expires_at) <= utcnow():
        raise AuthTokenError("Refresh token has expired.")

    user = session.get(UserRecord, record.user_id)
    if user is None or not user.is_active:
        raise AuthTokenError("Account is unavailable.")

    record.revoked_at = utcnow()
    access_token = create_access_token(user)
    new_refresh_token = generate_refresh_token()
    session.add(
        RefreshTokenRecord(
            user_id=user.id,
            token_hash=hash_refresh_token(new_refresh_token),
            expires_at=utcnow() + timedelta(days=refresh_token_days()),
        )
    )
    session.commit()
    return TokenPair(
        access_token=access_token,
        refresh_token=new_refresh_token,
        expires_in=access_token_seconds(),
        user=_user_read(user),
    )


def revoke_refresh_token(session: Session, raw_refresh_token: str) -> bool:
    token_hash = hash_refresh_token(raw_refresh_token)
    record = session.scalar(
        select(RefreshTokenRecord).where(RefreshTokenRecord.token_hash == token_hash)
    )
    if record is None:
        return False
    if record.revoked_at is None:
        record.revoked_at = utcnow()
        session.commit()
    return True
