from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class User:
    """User domain entity."""
    id: Optional[str] = None
    email: str = ""
    username: str = ""
    hashed_password: str = ""
    is_active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        """Validate the user entity."""
        if not self.email or not self.email.strip():
            raise ValueError("User email cannot be empty")
        if not self.username or not self.username.strip():
            raise ValueError("User username cannot be empty")
        if "@" not in self.email:
            raise ValueError("Invalid email format")

    def deactivate(self) -> None:
        """Deactivate the user."""
        self.is_active = False

    def activate(self) -> None:
        """Activate the user."""
        self.is_active = True

    def update_password(self, hashed_password: str) -> None:
        """Update user password."""
        if not hashed_password or not hashed_password.strip():
            raise ValueError("Password cannot be empty")
        self.hashed_password = hashed_password

    def update_profile(self, email: str = None, username: str = None) -> None:
        """Update user profile information."""
        if email is not None:
            if not email or not email.strip():
                raise ValueError("User email cannot be empty")
            if "@" not in email:
                raise ValueError("Invalid email format")
            self.email = email
            
        if username is not None:
            if not username or not username.strip():
                raise ValueError("User username cannot be empty")
            self.username = username

    def change_password(self, new_hashed_password: str) -> None:
        """Change user password."""
        if not new_hashed_password or not new_hashed_password.strip():
            raise ValueError("New password cannot be empty")
        self.hashed_password = new_hashed_password