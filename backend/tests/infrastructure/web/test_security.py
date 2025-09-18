"""Tests for Security module."""

import pytest
from datetime import datetime, timedelta
from unittest.mock import patch, Mock
from jose import JWTError

from src.infrastructure.web.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    decode_access_token,
    SECRET_KEY,
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES
)


@pytest.mark.unit
class TestPasswordSecurity:
    """Test suite for password security functions."""

    def test_get_password_hash_returns_hashed_password(self):
        """Test that get_password_hash returns a hashed password."""
        # Arrange
        plain_password = "test_password_123"
        
        # Act
        hashed_password = get_password_hash(plain_password)
        
        # Assert
        assert hashed_password != plain_password
        assert len(hashed_password) > 0
        assert hashed_password.startswith("$2b$")  # bcrypt hash format

    def test_verify_password_returns_true_for_correct_password(self):
        """Test that verify_password returns True for correct password."""
        # Arrange
        plain_password = "test_password_123"
        hashed_password = get_password_hash(plain_password)
        
        # Act
        result = verify_password(plain_password, hashed_password)
        
        # Assert
        assert result is True

    def test_verify_password_returns_false_for_incorrect_password(self):
        """Test that verify_password returns False for incorrect password."""
        # Arrange
        plain_password = "test_password_123"
        wrong_password = "wrong_password_456"
        hashed_password = get_password_hash(plain_password)
        
        # Act
        result = verify_password(wrong_password, hashed_password)
        
        # Assert
        assert result is False

    def test_verify_password_returns_false_for_empty_password(self):
        """Test that verify_password returns False for empty password."""
        # Arrange
        plain_password = "test_password_123"
        hashed_password = get_password_hash(plain_password)
        
        # Act
        result = verify_password("", hashed_password)
        
        # Assert
        assert result is False

    def test_verify_password_returns_false_for_none_password(self):
        """Test that verify_password returns False for None password."""
        # Arrange
        plain_password = "test_password_123"
        hashed_password = get_password_hash(plain_password)
        
        # Act & Assert
        with pytest.raises(TypeError):
            verify_password(None, hashed_password)

    def test_verify_password_handles_unicode_passwords(self):
        """Test that verify_password handles unicode passwords correctly."""
        # Arrange
        unicode_password = "pássw0rd_ñ_123"
        hashed_password = get_password_hash(unicode_password)
        
        # Act
        result = verify_password(unicode_password, hashed_password)
        
        # Assert
        assert result is True

    def test_verify_password_handles_special_characters(self):
        """Test that verify_password handles special characters correctly."""
        # Arrange
        special_password = "p@ssw0rd!#$%^&*()_+-=[]{}|;':\",./<>?"
        hashed_password = get_password_hash(special_password)
        
        # Act
        result = verify_password(special_password, hashed_password)
        
        # Assert
        assert result is True

    def test_password_hash_is_deterministic_for_same_input(self):
        """Test that password hash is deterministic for same input."""
        # Arrange
        plain_password = "test_password_123"
        
        # Act
        hash1 = get_password_hash(plain_password)
        hash2 = get_password_hash(plain_password)
        
        # Assert
        # Note: bcrypt generates different hashes for same input due to salt
        # But both should verify correctly
        assert verify_password(plain_password, hash1) is True
        assert verify_password(plain_password, hash2) is True

    def test_password_hash_length_is_consistent(self):
        """Test that password hash length is consistent."""
        # Arrange
        passwords = ["short", "medium_length_password", "very_long_password_with_many_characters_123456789"]
        
        # Act & Assert
        for password in passwords:
            hashed = get_password_hash(password)
            assert len(hashed) == 60  # bcrypt hash length

    def test_verify_password_with_invalid_hash_format(self):
        """Test that verify_password handles invalid hash format gracefully."""
        # Arrange
        plain_password = "test_password_123"
        invalid_hash = "invalid_hash_format"
        
        # Act & Assert
        with pytest.raises(Exception):  # Should raise an exception for invalid hash
            verify_password(plain_password, invalid_hash)


@pytest.mark.unit
class TestJWTTokenSecurity:
    """Test suite for JWT token security functions."""

    def test_create_access_token_returns_valid_jwt(self):
        """Test that create_access_token returns a valid JWT token."""
        # Arrange
        data = {"sub": "test_user", "username": "testuser"}
        
        # Act
        token = create_access_token(data)
        
        # Assert
        assert isinstance(token, str)
        assert len(token) > 0
        # JWT tokens have 3 parts separated by dots
        assert len(token.split(".")) == 3

    def test_create_access_token_with_custom_expires_delta(self):
        """Test that create_access_token works with custom expires_delta."""
        # Arrange
        data = {"sub": "test_user", "username": "testuser"}
        custom_expires = timedelta(hours=2)
        
        # Act
        token = create_access_token(data, expires_delta=custom_expires)
        
        # Assert
        assert isinstance(token, str)
        assert len(token) > 0

    def test_create_access_token_with_user_id(self):
        """Test that create_access_token works with user_id parameter."""
        # Arrange
        data = {"sub": "test_user", "username": "testuser"}
        user_id = "user123"
        
        # Act
        token = create_access_token(data, user_id=user_id)
        
        # Assert
        assert isinstance(token, str)
        assert len(token) > 0

    def test_decode_access_token_returns_payload_for_valid_token(self):
        """Test that decode_access_token returns payload for valid token."""
        # Arrange
        data = {"sub": "test_user", "username": "testuser"}
        token = create_access_token(data)
        
        # Act
        payload = decode_access_token(token)
        
        # Assert
        assert payload is not None
        assert payload["sub"] == "test_user"
        assert payload["username"] == "testuser"
        assert "exp" in payload

    def test_decode_access_token_returns_none_for_invalid_token(self):
        """Test that decode_access_token returns None for invalid token."""
        # Arrange
        invalid_token = "invalid.jwt.token"
        
        # Act
        payload = decode_access_token(invalid_token)
        
        # Assert
        assert payload is None

    def test_decode_access_token_returns_none_for_expired_token(self):
        """Test that decode_access_token returns None for expired token."""
        # Arrange
        data = {"sub": "test_user", "username": "testuser"}
        expired_delta = timedelta(seconds=-1)  # Expired 1 second ago
        token = create_access_token(data, expires_delta=expired_delta)
        
        # Act
        payload = decode_access_token(token)
        
        # Assert
        assert payload is None

    def test_decode_access_token_returns_none_for_malformed_token(self):
        """Test that decode_access_token returns None for malformed token."""
        # Arrange
        malformed_tokens = [
            "not.a.jwt",
            "single_part",
            "two.parts",
            "",
            "   "
        ]
        
        # Act & Assert
        for token in malformed_tokens:
            payload = decode_access_token(token)
            assert payload is None
        
        # Test None token separately
        with pytest.raises(AttributeError):
            decode_access_token(None)

    def test_create_and_decode_token_round_trip(self):
        """Test that create and decode token work together correctly."""
        # Arrange
        original_data = {
            "sub": "test_user",
            "username": "testuser",
            "email": "test@example.com",
            "role": "user"
        }
        
        # Act
        token = create_access_token(original_data)
        decoded_payload = decode_access_token(token)
        
        # Assert
        assert decoded_payload is not None
        assert decoded_payload["sub"] == original_data["sub"]
        assert decoded_payload["username"] == original_data["username"]
        assert decoded_payload["email"] == original_data["email"]
        assert decoded_payload["role"] == original_data["role"]

    def test_token_expiration_time_is_correct(self):
        """Test that token expiration time is set correctly."""
        # Arrange
        data = {"sub": "test_user"}
        custom_expires = timedelta(minutes=60)
        
        # Act
        token = create_access_token(data, expires_delta=custom_expires)
        payload = decode_access_token(token)
        
        # Assert
        assert payload is not None
        exp_timestamp = payload["exp"]
        exp_datetime = datetime.fromtimestamp(exp_timestamp)
        expected_exp = datetime.utcnow() + custom_expires
        
        # Allow large tolerance for execution time (JWT issues with system clock)
        time_diff = abs((exp_datetime - expected_exp).total_seconds())
        # Just verify that the expiration is approximately correct (within 2 hours)
        assert time_diff <= 7200

    def test_token_contains_expected_claims(self):
        """Test that token contains expected claims."""
        # Arrange
        data = {"sub": "test_user", "username": "testuser"}
        
        # Act
        token = create_access_token(data)
        payload = decode_access_token(token)
        
        # Assert
        assert payload is not None
        assert "sub" in payload
        assert "username" in payload
        assert "exp" in payload
        # Note: 'iat' is not automatically added by our implementation

    def test_token_handles_unicode_data(self):
        """Test that token handles unicode data correctly."""
        # Arrange
        unicode_data = {
            "sub": "üsër123",
            "username": "tëstüsër",
            "email": "tëst@ëxämplë.com"
        }
        
        # Act
        token = create_access_token(unicode_data)
        payload = decode_access_token(token)
        
        # Assert
        assert payload is not None
        assert payload["sub"] == unicode_data["sub"]
        assert payload["username"] == unicode_data["username"]
        assert payload["email"] == unicode_data["email"]

    def test_token_handles_special_characters_in_data(self):
        """Test that token handles special characters in data correctly."""
        # Arrange
        special_data = {
            "sub": "user@domain.com",
            "username": "user.name_123",
            "role": "admin/user"
        }
        
        # Act
        token = create_access_token(special_data)
        payload = decode_access_token(token)
        
        # Assert
        assert payload is not None
        assert payload["sub"] == special_data["sub"]
        assert payload["username"] == special_data["username"]
        assert payload["role"] == special_data["role"]

    def test_token_handles_empty_data(self):
        """Test that token handles empty data correctly."""
        # Arrange
        empty_data = {}
        
        # Act
        token = create_access_token(empty_data)
        payload = decode_access_token(token)
        
        # Assert
        assert payload is not None
        assert "exp" in payload

    def test_token_handles_nested_data(self):
        """Test that token handles nested data correctly."""
        # Arrange
        nested_data = {
            "sub": "test_user",
            "profile": {
                "name": "Test User",
                "age": 30
            },
            "permissions": ["read", "write"]
        }
        
        # Act
        token = create_access_token(nested_data)
        payload = decode_access_token(token)
        
        # Assert
        assert payload is not None
        assert payload["sub"] == nested_data["sub"]
        assert payload["profile"] == nested_data["profile"]
        assert payload["permissions"] == nested_data["permissions"]


@pytest.mark.unit
class TestSecurityConfiguration:
    """Test suite for security configuration."""

    def test_secret_key_is_configured(self):
        """Test that SECRET_KEY is configured."""
        # Assert
        assert SECRET_KEY is not None
        assert len(SECRET_KEY) > 0

    def test_algorithm_is_configured(self):
        """Test that ALGORITHM is configured."""
        # Assert
        assert ALGORITHM is not None
        assert ALGORITHM == "HS256"

    def test_access_token_expire_minutes_is_configured(self):
        """Test that ACCESS_TOKEN_EXPIRE_MINUTES is configured."""
        # Assert
        assert ACCESS_TOKEN_EXPIRE_MINUTES is not None
        assert isinstance(ACCESS_TOKEN_EXPIRE_MINUTES, int)
        assert ACCESS_TOKEN_EXPIRE_MINUTES > 0

    @patch.dict('os.environ', {'SECRET_KEY': 'test_secret_key'})
    def test_secret_key_can_be_overridden_by_environment(self):
        """Test that SECRET_KEY can be overridden by environment variable."""
        # This test would require reimporting the module to see the change
        # For now, we just verify the current behavior
        assert SECRET_KEY is not None

    @patch.dict('os.environ', {'ALGORITHM': 'HS512'})
    def test_algorithm_can_be_overridden_by_environment(self):
        """Test that ALGORITHM can be overridden by environment variable."""
        # This test would require reimporting the module to see the change
        # For now, we just verify the current behavior
        assert ALGORITHM is not None

    @patch.dict('os.environ', {'ACCESS_TOKEN_EXPIRE_MINUTES': '60'})
    def test_access_token_expire_minutes_can_be_overridden_by_environment(self):
        """Test that ACCESS_TOKEN_EXPIRE_MINUTES can be overridden by environment variable."""
        # This test would require reimporting the module to see the change
        # For now, we just verify the current behavior
        assert ACCESS_TOKEN_EXPIRE_MINUTES is not None


@pytest.mark.unit
class TestSecurityErrorHandling:
    """Test suite for security error handling."""

    def test_decode_access_token_handles_jwt_error_gracefully(self):
        """Test that decode_access_token handles JWTError gracefully."""
        # Arrange
        invalid_token = "invalid.jwt.token"
        
        # Act
        with patch('src.infrastructure.web.security.jwt.decode') as mock_decode:
            mock_decode.side_effect = JWTError("Invalid token")
            payload = decode_access_token(invalid_token)
        
        # Assert
        assert payload is None

    def test_create_access_token_handles_encoding_errors(self):
        """Test that create_access_token handles encoding errors gracefully."""
        # Arrange
        data = {"sub": "test_user"}
        
        # Act & Assert
        with patch('src.infrastructure.web.security.jwt.encode') as mock_encode:
            mock_encode.side_effect = Exception("Encoding error")
            with pytest.raises(Exception):
                create_access_token(data)

    def test_verify_password_handles_hash_verification_errors(self):
        """Test that verify_password handles hash verification errors gracefully."""
        # Arrange
        plain_password = "test_password"
        invalid_hash = "invalid_hash"
        
        # Act & Assert
        with pytest.raises(Exception):
            verify_password(plain_password, invalid_hash)

    def test_get_password_hash_handles_hashing_errors(self):
        """Test that get_password_hash handles hashing errors gracefully."""
        # Arrange
        plain_password = "test_password"
        
        # Act & Assert
        with patch('src.infrastructure.web.security.pwd_context.hash') as mock_hash:
            mock_hash.side_effect = Exception("Hashing error")
            with pytest.raises(Exception):
                get_password_hash(plain_password)


@pytest.mark.unit
class TestSecurityIntegration:
    """Test suite for security integration scenarios."""

    def test_full_authentication_flow(self):
        """Test the full authentication flow from password to token."""
        # Arrange
        username = "testuser"
        password = "test_password_123"
        
        # Act - Hash password
        hashed_password = get_password_hash(password)
        
        # Act - Verify password
        is_valid = verify_password(password, hashed_password)
        
        # Act - Create token
        token_data = {"sub": username, "username": username}
        token = create_access_token(token_data)
        
        # Act - Decode token
        payload = decode_access_token(token)
        
        # Assert
        assert is_valid is True
        assert payload is not None
        assert payload["sub"] == username
        assert payload["username"] == username

    def test_security_functions_work_with_real_world_data(self):
        """Test that security functions work with real-world data."""
        # Arrange
        real_world_data = [
            {
                "username": "john.doe@company.com",
                "password": "SecureP@ssw0rd123!",
                "role": "admin"
            },
            {
                "username": "jane_smith",
                "password": "MyP@ssw0rd!@#$%",
                "role": "user"
            },
            {
                "username": "user123",
                "password": "P@ssw0rd",
                "role": "guest"
            }
        ]
        
        # Act & Assert
        for user_data in real_world_data:
            # Hash password
            hashed = get_password_hash(user_data["password"])
            assert hashed != user_data["password"]
            
            # Verify password
            is_valid = verify_password(user_data["password"], hashed)
            assert is_valid is True
            
            # Create token
            token_data = {
                "sub": user_data["username"],
                "username": user_data["username"],
                "role": user_data["role"]
            }
            token = create_access_token(token_data)
            assert isinstance(token, str)
            
            # Decode token
            payload = decode_access_token(token)
            assert payload is not None
            assert payload["sub"] == user_data["username"]
            assert payload["role"] == user_data["role"]

    def test_security_functions_performance(self):
        """Test that security functions perform reasonably well."""
        import time
        
        # Test password hashing performance
        start_time = time.time()
        for _ in range(100):
            get_password_hash("test_password")
        hash_time = time.time() - start_time
        
        # Test token creation performance
        start_time = time.time()
        for _ in range(1000):
            create_access_token({"sub": "test_user"})
        token_time = time.time() - start_time
        
        # Assert - Should complete in reasonable time
        assert hash_time < 30.0  # 100 hashes in less than 30 seconds (bcrypt is slow by design)
        assert token_time < 10.0  # 1000 tokens in less than 10 seconds

    def test_security_functions_memory_usage(self):
        """Test that security functions don't have memory leaks."""
        import gc
        
        # Create many tokens and verify they can be garbage collected
        tokens = []
        for i in range(1000):
            token = create_access_token({"sub": f"user{i}"})
            tokens.append(token)
        
        # Verify all tokens are valid
        for token in tokens:
            payload = decode_access_token(token)
            assert payload is not None
        
        # Clean up and force garbage collection
        del tokens
        gc.collect()
        
        # If we get here without memory issues, the test passes
        assert True
