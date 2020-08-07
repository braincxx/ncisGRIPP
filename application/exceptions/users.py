from .base import AppError


class BadAccessError(AppError):
    pass


class UserNotFoundError(AppError):
    pass


class UserAlreadyAuthorizedError(AppError):
    pass


class UserAlreadyExistsError(AppError):
    pass


class UserDataValidationError(AppError):
    pass
