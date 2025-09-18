#!/usr/bin/env python3
"""Script to create a new test user for development."""

import asyncio
import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.infrastructure.adapters.repositories.mongodb_user_repository import MongoDBUserRepository
from src.infrastructure.web.security import get_password_hash
from src.domain.entities.user import User

async def create_new_test_user():
    """Create a new test user."""
    user_repo = MongoDBUserRepository()
    
    # New test user data
    email = "demo@example.com"
    username = "demo"
    password = "demo123"
    
    try:
        # Check if user already exists
        existing_user = await user_repo.find_by_email(email)
        if existing_user:
            print(f"User with email {email} already exists")
            return
        
        existing_user = await user_repo.find_by_username(username)
        if existing_user:
            print(f"User with username {username} already exists")
            return
        
        # Create new user
        hashed_password = get_password_hash(password)
        user = User(
            email=email,
            username=username,
            hashed_password=hashed_password
        )
        
        created_user = await user_repo.create(user)
        print(f"New test user created successfully:")
        print(f"  Email: {created_user.email}")
        print(f"  Username: {created_user.username}")
        print(f"  Password: {password}")
        print(f"  ID: {created_user.id}")
        
    except Exception as e:
        print(f"Error creating test user: {e}")

if __name__ == "__main__":
    asyncio.run(create_new_test_user())
