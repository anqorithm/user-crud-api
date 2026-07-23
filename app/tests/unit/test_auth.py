import pytest


class TestJWTAuthentication:
    """Tests for JWT authentication - token creation and validation"""

    def test_token_creation_works(self):
        from app.core.security import create_access_token
        token = create_access_token({"sub": "user123"})
        assert token is not None
        assert isinstance(token, str)

    def test_token_decoding_works(self):
        from app.core.security import create_access_token, decode_token
        token = create_access_token({"sub": "user123"})
        decoded = decode_token(token)
        assert decoded["sub"] == "user123"

    def test_invalid_token_raises_exception(self):
        from app.core.security import decode_token
        from app.core.exceptions import UnauthorizedException
        with pytest.raises(UnauthorizedException):
            decode_token("invalid")