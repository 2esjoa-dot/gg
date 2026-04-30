"""Unit tests for security utilities (bcrypt, JWT)."""

from datetime import timedelta

import pytest

from app.utils.security import create_access_token, decode_access_token, hash_password, verify_password


class TestPasswordHashing:
    """Tests for bcrypt password hashing and verification."""

    def test_hash_password_returns_hash(self):
        hashed = hash_password("test1234")
        assert hashed != "test1234"
        assert hashed.startswith("$2b$")

    def test_verify_correct_password(self):
        hashed = hash_password("mypassword")
        assert verify_password("mypassword", hashed) is True

    def test_verify_wrong_password(self):
        hashed = hash_password("mypassword")
        assert verify_password("wrongpassword", hashed) is False

    def test_different_hashes_for_same_password(self):
        hash1 = hash_password("same")
        hash2 = hash_password("same")
        assert hash1 != hash2  # bcrypt uses random salt


class TestJWT:
    """Tests for JWT token creation and decoding."""

    def test_create_and_decode_token(self):
        data = {"user_id": 1, "store_id": 2, "role": "store_admin"}
        token = create_access_token(data)
        decoded = decode_access_token(token)
        assert decoded is not None
        assert decoded["user_id"] == 1
        assert decoded["store_id"] == 2
        assert decoded["role"] == "store_admin"

    def test_expired_token_returns_none(self):
        data = {"user_id": 1}
        token = create_access_token(data, expires_delta=timedelta(seconds=-1))
        decoded = decode_access_token(token)
        assert decoded is None

    def test_invalid_token_returns_none(self):
        decoded = decode_access_token("invalid.token.here")
        assert decoded is None

    def test_token_contains_exp_claim(self):
        token = create_access_token({"user_id": 1})
        decoded = decode_access_token(token)
        assert "exp" in decoded
