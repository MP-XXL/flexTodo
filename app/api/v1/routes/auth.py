# from fastapi import APIRouter, Depends, status
# from sqlalchemy.orm import Session

# from app.db.session import get_db
# from app.schemas.auth import (
#     RegisterResponse,
#     TokenResponse,
#     UserLoginRequest,
#     UserRegisterRequest,
#     UserResponse,
# )
# from app.services import auth_service

# router = APIRouter(prefix="/auth", tags=["Authentication"])


# @router.post(
#     "/register",
#     response_model=RegisterResponse,
#     status_code=status.HTTP_201_CREATED,
#     summary="Register a new user",
# )
# def register(payload: UserRegisterRequest, db: Session = Depends(get_db)):
#     user = auth_service.register_user(payload, db)
#     return RegisterResponse(
#         message="Account created successfully.",
#         user=UserResponse.model_validate(user),
#     )


# @router.post(
#     "/login",
#     response_model=TokenResponse,
#     status_code=status.HTTP_200_OK,
#     summary="Authenticate and receive a JWT access token",
# )
# def login(payload: UserLoginRequest, db: Session = Depends(get_db)):
#     access_token = auth_service.login_user(payload, db)
#     return TokenResponse(access_token=access_token)


from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.auth import (
    RegisterResponse,
    TokenResponse,
    UserLoginRequest,
    UserRegisterRequest,
    UserResponse,
)
from app.services import auth_service

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/register",
    response_model=RegisterResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
)
def register(payload: UserRegisterRequest, db: Session = Depends(get_db)):
    user = auth_service.register_user(payload, db)
    return RegisterResponse(
        message="Account created successfully.",
        user=UserResponse.model_validate(user),
    )


@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Authenticate and receive a JWT access token",
)
def login(payload: UserLoginRequest, db: Session = Depends(get_db)):
    access_token = auth_service.login_user(payload, db)
    return TokenResponse(access_token=access_token)


@router.get(
    "/me",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Get the currently authenticated user's profile",
)
def me(current_user: User = Depends(get_current_user)):
    return UserResponse.model_validate(current_user)
