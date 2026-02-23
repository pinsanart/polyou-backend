from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from .core.config.config import settings
from .routes import (
    auth, 
    users, 
    languages, 
    flashcards
)

import app.dependencies.sqlalchemy.registrations.repositories
import app.dependencies.sqlalchemy.registrations.mappers
import app.dependencies.sqlalchemy.registrations.services

from .core.exceptions.jwt import (
    JWTTokenMissingSubjectError,
    JWTInvalidTokenError,
    JWTTokenExpiredSignatureError
)

from .core.exceptions.auth import (
    InvalidCredentials,
    UserDisabled,
    UserNotFound,

    RefreshTokenExpiredError,
    RefreshTokenNotFoundError,
    RefreshTokenRevokedError
) 

from .core.exceptions.languages import (
    LanguageNotAvailableError
)

from .core.exceptions.user import (
    EmailAlreadyExistsError,
    UserDoesNotExist
)

from .core.exceptions.user_flashcard_target import (
    TargetLanguageAlreadyExistsError,
    NotAddedTargetLanguage
)

from .core.exceptions.flashcards import (
    PublicIDDoesNotBelongToUserError,
    PublicIDAlreadyRegistedError,
    PublicIDDoesNotExistError
)

app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(languages.router)
app.include_router(flashcards.router)

@app.exception_handler(JWTInvalidTokenError)
async def invalid_jwt_token_handler(request: Request, exc: JWTInvalidTokenError):
    return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"detail": str(exc.message)})

@app.exception_handler(JWTTokenExpiredSignatureError)
async def expired_signature_jwt_token_handler(request: Request, exc: JWTTokenExpiredSignatureError):
    return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"detail": str(exc.message)})

@app.exception_handler(JWTTokenMissingSubjectError)
async def user_not_found_handler(request: Request, exc: JWTTokenMissingSubjectError):
    return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"detail": str(exc.message)})

@app.exception_handler(InvalidCredentials)
async def invalid_credentials_handler(request: Request, exc: InvalidCredentials):
    return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"detail": str(exc.message)})

@app.exception_handler(UserDisabled)
async def user_disabled_handler(request: Request, exc: UserDisabled):
    return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"detail": str(exc.message)})

@app.exception_handler(UserNotFound)
async def user_not_found_handler(request: Request, exc: UserNotFound):
    return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"detail": str(exc.message)})

@app.exception_handler(LanguageNotAvailableError)
async def language_not_available_handler(request: Request, exc: LanguageNotAvailableError):
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": str(exc.message)})

@app.exception_handler(EmailAlreadyExistsError)
async def email_already_exists_handler(request: Request, exc: EmailAlreadyExistsError):
    return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"detail": str(exc.message)})

@app.exception_handler(TargetLanguageAlreadyExistsError)
async def target_language_already_exists_handler(request: Request, exc: TargetLanguageAlreadyExistsError):
    return JSONResponse(status_code=status.HTTP_406_NOT_ACCEPTABLE, content={"detail": str(exc.message)})

@app.exception_handler(NotAddedTargetLanguage)
async def not_added_target_language_handler(request: Request, exc: NotAddedTargetLanguage):
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": str(exc.message)})

@app.exception_handler(PublicIDDoesNotBelongToUserError)
async def public_id_does_not_belong_to_user_handler(request: Request, exc: PublicIDDoesNotBelongToUserError):
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": str(exc.message)})

@app.exception_handler(UserDoesNotExist)
async def user_does_not_exist_handler(request: Request, exc: UserDoesNotExist):
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": str(exc.message)})

@app.exception_handler(PublicIDAlreadyRegistedError)
async def public_id_already_registed_handler(request: Request, exc: PublicIDAlreadyRegistedError):
    return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"detail": str(exc.message)})

@app.exception_handler(PublicIDDoesNotExistError)
async def public_id_does_not_exist_handler(request: Request, exc: PublicIDDoesNotExistError):
    return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"detail": str(exc.message)})

@app.exception_handler(RefreshTokenExpiredError)
async def refresh_token_expired_handler(request: Request, exc: RefreshTokenExpiredError):
    return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"detail": str(exc.message)})

@app.exception_handler(RefreshTokenNotFoundError)
async def refresh_token_not_found_handler(request: Request, exc: RefreshTokenNotFoundError):
    return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"detail": str(exc.message)})

@app.exception_handler(RefreshTokenRevokedError)
async def refresh_token_revoked_handler(request: Request, exc: RefreshTokenRevokedError):
    return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"detail": str(exc.message)})