class AppError(Exception):
    """Base application error"""
    pass


class NotFoundError(AppError):
    """Raised when a resource is not found"""
    pass


class ValidationError(AppError):
    """Raised for input validation errors"""
    pass
