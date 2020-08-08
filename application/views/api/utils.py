from application.exceptions import DataValidationError
from application.exceptions.requests import PageNotFoundError


def handle_bad_requests(func):
    def handle_bad_requests_internal(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except DataValidationError as error:
            error_message = "Data validation error: " + ", ".\
                join(["{} ({})".format(field, message)for field, message in error.errors.items()])

            return Error(error_message), 400
        except PageNotFoundError as error:
            return Error("Page not found"), 404
        except Exception as error:
            return Error("Invalid request error"), 400

    return handle_bad_requests_internal
