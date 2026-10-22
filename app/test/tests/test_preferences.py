import os

# Ensure these variables point to a dedicated test database.
os.environ.setdefault(
    "DATABASE_URL",
    "postgresql+psycopg://notification_user:local_dev_password@localhost:5432/notification_db",
)
os.environ.setdefault(
    "JWT_SECRET",
    "test-only-secret-change-this-before-production",
)

from fastapi.testclient import TestClient

from app.auth import create_access_token
from app.main import app


client = TestClient(app)


def token_for(user_id: int) -> dict[str, str]:
    token = create_access_token(user_id)
    return {"Authorization": f"Bearer {token}"}


def test_user_can_read_own_preferences():
    # Alice is user ID 1 in the freshly seeded demo database.
    response = client.get(
        "/preferences/1",
        headers=token_for(1),
    )

    assert response.status_code == 200
    assert response.json()["user_id"] == 1


def test_user_cannot_read_another_users_preferences():
    # Bob owns preference 2. Alice is not an admin.
    response = client.get(
        "/preferences/2",
        headers=token_for(1),
    )

    assert response.status_code == 403


def test_admin_cannot_cross_tenant_boundary():
    # Bob is an admin in tenant 1. Preference 3 belongs to tenant 2.
    response = client.get(
        "/preferences/3",
        headers=token_for(2),
    )

    assert response.status_code == 404


def test_unauthenticated_request_is_rejected():
    response = client.get("/preferences/1")

    assert response.status_code == 401


def test_stale_update_is_rejected():
    headers = token_for(1)

    first = client.patch(
        "/preferences/1",
        headers=headers,
        json={
            "email_enabled": False,
            "version": 1,
        },
    )
    assert first.status_code == 200
    assert first.json()["version"] == 2

    second = client.patch(
        "/preferences/1",
        headers=headers,
        json={
            "sms_enabled": True,
            "version": 1,
        },
    )

    assert second.status_code == 409
