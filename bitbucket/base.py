import typing

from .exceptions import (
    InvalidIDError,
    NotAuthenticatedError,
    NotFoundIDError,
    PermissionError,
    UnknownError,
)


class BaseClient(object):
    BASE_URL = "https://api.bitbucket.org/"

    def __init__(self, user: str, password: str, owner: typing.Union[str, None] = None):
        self.user = user
        self.password = password
        self.username = owner

    def parse(self, response) -> typing.Union[typing.Dict[str, typing.Any], None]:
        """
        Parses the response from the BitBucket API and returns the response data or raises an exception if the response
        indicates an error.

        Args:
            response: The response object returned by the BitBucket API.

        Returns:
            If the response status code is 200, 201, or 202, returns the JSON data in the response body as a dictionary.
            If the response status code is 204, returns None.
            Otherwise, raises an exception indicating the error message returned by the API.

        Raises:
            InvalidIDError: If the response status code is 400.
            NotAuthenticatedError: If the response status code is 401.
            PermissionError: If the response status code is 403.
            NotFoundIDError: If the response status code is 404.
            UnknownError: If the response status code is not one of the above.
        """
        status_code = response.status_code
        if "application/json" in response.headers["Content-Type"]:
            r = response.json()
        else:
            r = response.text
        if status_code in (200, 201, 202):
            return r
        if status_code == 204:
            return None
        message = None
        try:
            if type(r) == dict:
                message = r["error"]["message"]
            else:
                message = r
        except Exception:
            message = response.text
        if status_code == 400:
            raise InvalidIDError(message)
        if status_code == 401:
            raise NotAuthenticatedError(message)
        if status_code == 403:
            raise PermissionError(message)
        if status_code == 404:
            raise NotFoundIDError(message)
        raise UnknownError(message)
