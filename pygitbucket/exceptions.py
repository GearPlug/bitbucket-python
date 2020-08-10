class BaseError(Exception):
    pass


class UnknownError(BaseError):
    pass


class InvalidIDError(BaseError):
    pass


class NotFoundIDError(BaseError):
    pass


class NotAuthenticatedError(BaseError):
    pass


class PermissionError(BaseError):
    pass
