"""User and authentication routes."""

from datetime import timedelta
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from src.domain.exceptions.user import UserNotFoundError, UserAlreadyExistsError, InvalidCredentialsError
from src.infrastructure.web.dto.user_dto import UserCreate, UserResponse, Token, LogoutResponse, UserUpdate, ChangePasswordRequest
from src.infrastructure.web.dependencies import (
    get_all_users_use_case,
    get_user_by_id_use_case,
    get_create_user_use_case,
    get_authenticate_user_use_case,
    get_current_user,
    get_current_active_user,
    get_logout_user_use_case,
    get_update_user_use_case,
    get_change_password_use_case
)
from src.infrastructure.web.mappers import UserMapper
from src.infrastructure.web.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from src.application.use_cases.user_use_cases import (
    GetAllUsersUseCase,
    GetUserByIdUseCase,
    CreateUserUseCase,
    AuthenticateUserUseCase,
    LogoutUserUseCase
)
from src.domain.entities.user import User


router = APIRouter(tags=["users"])


@router.post("/auth/register", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate,
    create_user_use_case: CreateUserUseCase = Depends(get_create_user_use_case)
):
    """Register a new user."""
    try:
        hashed_password = get_password_hash(user_data.password)
        user = await create_user_use_case.execute(
            email=user_data.email,
            username=user_data.username,
            hashed_password=hashed_password
        )
        
        # Create access token for the new user
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )
        
        return Token(access_token=access_token)
    except UserAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create user: {str(e)}"
        )


@router.post("/auth/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    authenticate_user_use_case: AuthenticateUserUseCase = Depends(get_authenticate_user_use_case)
):
    """Login user and return JWT token."""
    user = await authenticate_user_use_case.execute(form_data.username)
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "user_id": user.id},
        expires_delta=access_token_expires,
    )
    
    return Token(access_token=access_token)


@router.post("/auth/logout", response_model=LogoutResponse)
async def logout(
    current_user: dict = Depends(get_current_active_user),
    logout_use_case: LogoutUserUseCase = Depends(get_logout_user_use_case)
):
    """Logout user and invalidate session."""
    try:
        success = await logout_use_case.execute(current_user["id"])
        return LogoutResponse(
            message="Successfully logged out",
            success=success
        )
    except UserNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Logout failed: {str(e)}"
        )


@router.get("/users/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_user)):
    """Get current user information."""
    return UserMapper.to_response(current_user)


@router.get("/users", response_model=List[UserResponse])
async def get_users(
    limit: int = 100,
    get_all_users_use_case: GetAllUsersUseCase = Depends(get_all_users_use_case),
    current_user: User = Depends(get_current_active_user)
):
    """Get all users (requires authentication)."""
    users = await get_all_users_use_case.execute(limit)
    return UserMapper.to_response_list(users)


@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: str,
    get_user_by_id_use_case: GetUserByIdUseCase = Depends(get_user_by_id_use_case),
    current_user: User = Depends(get_current_active_user)
):
    """Get user by ID (requires authentication)."""
    try:
        user = await get_user_by_id_use_case.execute(user_id)
        return UserMapper.to_response(user)
    except UserNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )


@router.put("/users/me", response_model=UserResponse)
async def update_user_profile(
    user_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    update_user_use_case = Depends(get_update_user_use_case)
):
    """Update current user profile information."""
    try:
        # Validate password confirmation if provided
        if hasattr(user_data, 'confirm_password') and user_data.new_password != user_data.confirm_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="New password and confirmation do not match"
            )
        
        updated_user = await update_user_use_case.execute(
            user_id=current_user.id,
            username=user_data.username,
            email=user_data.email
        )
        return UserMapper.to_response(updated_user)
    except UserNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    except UserAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update user: {str(e)}"
        )


@router.put("/users/me/password", response_model=dict)
async def change_password(
    password_data: ChangePasswordRequest,
    current_user: User = Depends(get_current_user),
    change_password_use_case = Depends(get_change_password_use_case)
):
    """Change user password."""
    try:
        # Validate password confirmation
        if password_data.new_password != password_data.confirm_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="New password and confirmation do not match"
            )
        
        await change_password_use_case.execute(
            user_id=current_user.id,
            current_password=password_data.current_password,
            new_password=password_data.new_password
        )
        
        return {"message": "Password changed successfully"}
    except UserNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    except InvalidCredentialsError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to change password: {str(e)}"
        )