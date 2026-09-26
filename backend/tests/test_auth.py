import pytest
from fastapi.testclient import TestClient
from sqlalchemy import delete, select

from app.database import SessionLocal
from app.main import app
from app.models import (
    AuditEventRecord,
    IncidentRecord,
    IncidentReportRecord,
    NotificationRecord,
    RefreshTokenRecord,
    UserRecord,
)


client = TestClient(app)
PASSWORD = "StrongPass123!"
TEAM_CODE = "verified-team-code"


@pytest.fixture(autouse=True)
def clean_auth_tables(monkeypatch):
    monkeypatch.setenv("RESPONSE_TEAM_REGISTRATION_CODE", TEAM_CODE)
    with SessionLocal.begin() as session:
        session.execute(delete(AuditEventRecord))
        session.execute(delete(IncidentReportRecord))
        session.execute(delete(IncidentRecord))
        session.execute(delete(RefreshTokenRecord))
        session.execute(delete(NotificationRecord))
        session.execute(delete(UserRecord))
    yield
    with SessionLocal.begin() as session:
        session.execute(delete(AuditEventRecord))
        session.execute(delete(IncidentReportRecord))
        session.execute(delete(IncidentRecord))
        session.execute(delete(RefreshTokenRecord))
        session.execute(delete(NotificationRecord))
        session.execute(delete(UserRecord))


def register(email="citizen@example.com", role="citizen", code=None):
    body = {
        "email": email,
        "display_name": "  Test User  ",
        "password": PASSWORD,
        "role": role,
    }
    if code is not None:
        body["response_team_verification_code"] = code
    return client.post("/v1/auth/register", json=body)


def login(email="citizen@example.com", password=PASSWORD):
    return client.post(
        "/v1/auth/login",
        json={"email": email, "password": password},
    )


def test_citizen_registration_hashes_password_and_normalizes_profile():
    response = register(email="Citizen@Example.COM")
    assert response.status_code == 201
    body = response.json()
    assert body["email"] == "citizen@example.com"
    assert body["display_name"] == "Test User"
    assert body["role"] == "citizen"
    assert body["is_verified"] is True

    with SessionLocal() as session:
        user = session.scalar(
            select(UserRecord).where(UserRecord.email == "citizen@example.com")
        )
        assert user is not None
        assert user.password_hash != PASSWORD
        assert user.password_hash.startswith("$argon2")


def test_duplicate_email_is_rejected_case_insensitively():
    assert register(email="same@example.com").status_code == 201
    response = register(email="SAME@example.com")
    assert response.status_code == 409


def test_login_and_me_return_authenticated_user():
    register()
    logged_in = login()
    assert logged_in.status_code == 200
    tokens = logged_in.json()
    assert tokens["token_type"] == "bearer"
    assert tokens["access_token"]
    assert tokens["refresh_token"]
    assert tokens["expires_in"] > 0

    me = client.get(
        "/v1/auth/me",
        headers={"Authorization": f"Bearer {tokens['access_token']}"},
    )
    assert me.status_code == 200
    assert me.json()["email"] == "citizen@example.com"


def test_invalid_password_is_rejected():
    register()
    response = login(password="WrongPass123!")
    assert response.status_code == 401


def test_me_requires_valid_access_token():
    assert client.get("/v1/auth/me").status_code == 401
    assert client.get(
        "/v1/auth/me",
        headers={"Authorization": "Bearer definitely-not-a-jwt"},
    ).status_code == 401


def test_refresh_token_rotation_invalidates_old_refresh_token():
    register()
    first = login().json()

    rotated = client.post(
        "/v1/auth/refresh",
        json={"refresh_token": first["refresh_token"]},
    )
    assert rotated.status_code == 200
    second = rotated.json()
    assert second["refresh_token"] != first["refresh_token"]
    assert second["access_token"] != first["access_token"]

    reused = client.post(
        "/v1/auth/refresh",
        json={"refresh_token": first["refresh_token"]},
    )
    assert reused.status_code == 401


def test_logout_revokes_refresh_token():
    register()
    tokens = login().json()

    logout = client.post(
        "/v1/auth/logout",
        json={"refresh_token": tokens["refresh_token"]},
    )
    assert logout.status_code == 200
    assert logout.json()["revoked"] is True

    refresh = client.post(
        "/v1/auth/refresh",
        json={"refresh_token": tokens["refresh_token"]},
    )
    assert refresh.status_code == 401


def test_response_team_is_unverified_without_registration_code():
    response = register(
        email="team@example.com",
        role="response_team",
    )
    assert response.status_code == 201
    assert response.json()["is_verified"] is False


def test_response_team_can_be_verified_with_configured_registration_code():
    response = register(
        email="team@example.com",
        role="response_team",
        code=TEAM_CODE,
    )
    assert response.status_code == 201
    assert response.json()["role"] == "response_team"
    assert response.json()["is_verified"] is True


def test_wrong_response_team_code_does_not_grant_verification():
    response = register(
        email="team@example.com",
        role="response_team",
        code="wrong-code",
    )
    assert response.status_code == 201
    assert response.json()["is_verified"] is False
