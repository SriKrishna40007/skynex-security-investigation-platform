from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from app.api.v1.dependencies.rbac import require_role

from app.api.v1.dependencies.auth import get_current_user
from app.application.auth import (
    LoginUserUseCase,
    LogoutSessionUseCase,
    RefreshSessionUseCase,
    RegisterUserUseCase,
    VerifyEmailUseCase,
)
from app.core.database import get_db
from app.core.logging import security_event
from app.exceptions import (
    InvalidCredentialsError,
    InvalidEmailVerificationTokenError,
    UserAlreadyExistsError,
)
from app.models.user import User
from app.repositories import (
    EmailVerificationTokenRepository,
    SessionRepository,
    UserRepository,
)
from app.schemas.auth import (
    LoginRequest,
    LogoutRequest,
    RefreshTokenRequest,
    RegisterRequest,
    RegisterResponse,
    VerifyEmailRequest,
    VerifyEmailResponse,
    TokenResponse,
    UserResponse,
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=RegisterResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(
    request: RegisterRequest,
    db: Session = Depends(get_db),
) -> RegisterResponse:
    user_repository = UserRepository(db)
    verification_repository = EmailVerificationTokenRepository(db)

    use_case = RegisterUserUseCase(
        user_repository,
        verification_repository,
    )

    try:
        return use_case.execute(request)
    except UserAlreadyExistsError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc


@router.post(
    "/verify-email",
    response_model=VerifyEmailResponse,
)
def verify_email(
    request: VerifyEmailRequest,
    db: Session = Depends(get_db),
) -> VerifyEmailResponse:
    user_repository = UserRepository(db)
    verification_repository = EmailVerificationTokenRepository(db)

    use_case = VerifyEmailUseCase(
        user_repository,
        verification_repository,
    )

    try:
        return use_case.execute(request.token)
    except InvalidEmailVerificationTokenError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    request: LoginRequest,
    http_request: Request,
    db: Session = Depends(get_db),
) -> TokenResponse:
    user_repository = UserRepository(db)
    session_repository = SessionRepository(db)

    use_case = LoginUserUseCase(
        user_repository,
        session_repository,
    )

    client_host = http_request.client.host if http_request.client is not None else None

    user_agent = http_request.headers.get("user-agent")

    try:
        response = use_case.execute(
            request,
            ip_address=client_host,
            user_agent=user_agent,
        )

        security_event(
            "auth.login",
            success=True,
            ip_address=client_host,
            user_agent=user_agent,
        )

        return response
    except InvalidCredentialsError as exc:
        security_event(
            "auth.login",
            success=False,
            ip_address=client_host,
            reason="invalid_credentials",
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
        ) from exc


@router.post(
    "/refresh",
    response_model=TokenResponse,
)
def refresh_session(
    request: RefreshTokenRequest,
    db: Session = Depends(get_db),
) -> TokenResponse:
    user_repository = UserRepository(db)
    session_repository = SessionRepository(db)

    use_case = RefreshSessionUseCase(
        user_repository,
        session_repository,
    )

    try:
        return use_case.execute(request.refresh_token)
    except InvalidCredentialsError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
        ) from exc


@router.post(
    "/logout",
    status_code=status.HTTP_204_NO_CONTENT,
)
def logout(
    request: LogoutRequest,
    db: Session = Depends(get_db),
) -> None:
    session_repository = SessionRepository(db)
    use_case = LogoutSessionUseCase(session_repository)

    try:
        use_case.execute(request.refresh_token)

        security_event(
            "auth.logout",
            success=True,
        )
    except InvalidCredentialsError as exc:
        security_event(
            "auth.logout",
            success=False,
            reason="invalid_refresh_token",
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
        ) from exc


@router.get(
    "/me",
    response_model=UserResponse,
)
def me(
    current_user: User = Depends(get_current_user),
) -> UserResponse:
    return UserResponse.model_validate(current_user)


@router.get("/admin")
def admin_only(
    current_user=Depends(require_role("admin")),
):
    return {
        "message": f"Welcome {current_user.full_name}",
        "role": current_user.role.name,
    }
