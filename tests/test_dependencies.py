import pytest
from fastapi import HTTPException
from app.security.dependencies import get_current_user

from jose import jwt
from datetime import datetime, timedelta
from app.config import settings


def generate_token(sub="user", role="admin", expired=False):
    expire_time = datetime.utcnow() - timedelta(minutes=1) if expired else datetime.utcnow() + timedelta(minutes=10)
    payload = {"sub": sub, "role": role, "exp": expire_time}
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


def test_get_current_user_valid():
    token = generate_token()
    result = get_current_user(token)
    assert result["user_id"] == "user"
    assert result["role"] == "admin"


def test_get_current_user_missing_sub():
    token = jwt.encode({"exp": datetime.utcnow() + timedelta(minutes=10)}, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

    with pytest.raises(HTTPException) as exc:
        get_current_user(token)
    assert exc.value.status_code == 401


def test_get_current_user_invalid_token():
    with pytest.raises(HTTPException):
        get_current_user("this.is.invalid")
