
class AppException(Exception):
    """Base exception for all application errors."""

    def __init__(
        self,
        message: str,
        status_code: int = 500,
        error_code: str = "APPLICATION_ERROR",
    ):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code

        super().__init__(message)


class AuthenticationError(AppException):
    """Raised when authentication fails."""

    def __init__(
        self,   
        message: str = "Authentication failed",
        error_code: str = "AUTHENTICATION_FAILED",
    ):
        super().__init__(message, 401, error_code)


class PermissionDeniedError(AppException):
    """Raised when a user lacks required permission."""

    def __init__(
        self,
        message: str = "Permission denied",
        error_code: str = "PERMISSI ON_DENIED",
    ):
        super().__init__(message, 403, error_code)


class ResourceNotFoundError(AppException):
    """Raised when a requested resource does not exist."""

    def __init__(
        self,
        message: str = "Resource not found",
        error_code: str = "RESOURCE_NOT_FOUND",
    ):
        super().__init__(message, 404, error_code)


class ConflictError(AppException):
    """Raised when a resource conflicts with existing data."""

    def __init__(
        self,
        message: str = "Resource already exists",
        error_code: str = "RESOURCE_CONFLICT",
    ):
        super().__init__(message, 409, error_code)


class ExternalServiceError(AppException):
    """Raised when an external service operation fails."""

    def __init__(
        self,
        message: str = "External service error",
        error_code: str = "EXTERNAL_SERVICE_ERROR",
    ):
        super().__init__(message, 502, error_code)
