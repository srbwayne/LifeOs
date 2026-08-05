from fastapi import APIRouter, Depends, HTTPException, status, Request, Response
from app.auth.application.commands.register_user import RegisterUserCommand, RegisterUserCommandHandler
from app.auth.application.commands.login import LoginCommand, LoginCommandHandler
from app.auth.application.commands.logout import LogoutCommand, LogoutCommandHandler
from app.auth.application.commands.refresh_token import RefreshTokenCommand, RefreshTokenCommandHandler
from app.auth.application.commands.request_password_reset import RequestPasswordResetCommand, RequestPasswordResetCommandHandler
from app.auth.application.commands.reset_password import ResetPasswordCommand, ResetPasswordCommandHandler
from app.auth.presentation.api.fastapi.schemas import RegisterUserSchema, LoginSchema, TokenSchema, RefreshTokenSchema, RequestPasswordResetSchema, ResetPasswordSchema
from app.auth.dependencies import (
    get_login_handler,
    get_logout_handler,
    get_refresh_token_handler,
    get_request_password_reset_handler,
    get_reset_password_handler,
)
from app.composition_root import get_register_user_handler

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(
    schema: RegisterUserSchema,
    handler: RegisterUserCommandHandler = Depends(get_register_user_handler),
):
    command = RegisterUserCommand(email=schema.email, password=schema.password)
    handler(command)
    return {"message": "User registered successfully."}

@router.post("/login", response_model=TokenSchema)
def login(
    schema: LoginSchema,
    request: Request,
    response: Response,
    handler: LoginCommandHandler = Depends(get_login_handler),
):
    command = LoginCommand(
        email=schema.email,
        password=schema.password,
        user_agent=request.headers.get("User-Agent"),
        ip_address=request.client.host,
    )
    tokens = handler(command)
    response.set_cookie(
        key="refresh_token",
        value=tokens.refresh_token,
        httponly=True,
        samesite="strict",
        secure=False, # Em produção, deve ser True
    )
    return tokens

@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(
    request: Request,
    response: Response,
    handler: LogoutCommandHandler = Depends(get_logout_handler),
):
    refresh_token = request.cookies.get("refresh_token")
    if refresh_token:
        command = LogoutCommand(refresh_token=refresh_token)
        handler(command)
    response.delete_cookie(key="refresh_token")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.post("/refresh", response_model=TokenSchema)
def refresh(
    request: Request,
    response: Response,
    handler: RefreshTokenCommandHandler = Depends(get_refresh_token_handler),
):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No refresh token found.",
        )
    
    command = RefreshTokenCommand(refresh_token=refresh_token)
    new_tokens = handler(command)
    
    response.set_cookie(
        key="refresh_token",
        value=new_tokens.refresh_token,
        httponly=True,
        samesite="strict",
        secure=False, # Em produção, deve ser True
    )
    return new_tokens

@router.post("/request-password-reset", status_code=status.HTTP_202_ACCEPTED)
def request_password_reset(
    schema: RequestPasswordResetSchema,
    handler: RequestPasswordResetCommandHandler = Depends(get_request_password_reset_handler),
):
    command = RequestPasswordResetCommand(email=schema.email)
    handler(command)
    return {"message": "If a user with that email exists, a password reset link has been sent."}

@router.post("/reset-password", status_code=status.HTTP_204_NO_CONTENT)
def reset_password(
    schema: ResetPasswordSchema,
    handler: ResetPasswordCommandHandler = Depends(get_reset_password_handler),
):
    command = ResetPasswordCommand(token=schema.token, new_password=schema.new_password)
    handler(command)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
