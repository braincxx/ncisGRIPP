class AppError(Exception):
    pass


class AppInternalError(AppError):
    pass


class AppDataBaseError(AppError):
    pass


class DataValidationError(AppError):
    def __init__(self, errors):
        super().__init__()

        self.__errors = errors


    @property
    def errors(self):
        return self.__errors
