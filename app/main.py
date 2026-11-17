
from fastapi import FastAPI

from fastapi import Depends
from app.core.config import settings
from app.modules.auth.router import router as auth_router
from app.core.dependencies import get_current_user
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.modules.file.router import router as file_router
from app.core.exceptions import AppException
from app.core.exception_handlers import (
    app_exception_handler,
    general_exception_handler,
    http_exception_handler,
    validation_exception_handler,
)
app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG,
)



app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

app.include_router(auth_router)
app.include_router(file_router)

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "message": "Cloud Storage Reporting API is running",
    }

@app.get("/auth/me")
def get_my_profile(
    current_user: dict = Depends(get_current_user),
):
    return {
        "message": "Authentication successful",
        "user_id": current_user.get("sub"),
        "email": current_user.get("email"),
    }