import typing
import requests

from .exceptions import (
    InvalidIDError,
    NotAuthenticatedError,
    NotFoundIDError,
    PermissionError,
    UnknownError,
)


class BaseClient(object):
    BASE_URL = "https://api.bitbucket.org/"
    TOKEN_URL = 'https://bitbucket.org/site/oauth2/access_token'

    def __init__(self, user: str=None, password: str=None,token: str=None,client_id: str=None, client_secret: str=None, owner: typing.Union[str, None] = None):
        self.user = user
        self.password = password
        self.username = owner
        self.use_password = False
        self.use_token = False
        if user and password:
            self.use_password = True
        self.token = token
        if token:
            self.use_token = True
        elif client_id and client_secret:
            token_req_payload = {'grant_type': 'client_credentials'}
            response = requests.post(self.TOKEN_URL, data=token_req_payload, allow_redirects=False, auth=(client_id, client_secret))
            response = self._parse(response)
            self.token = response['access_token']
            self.use_token = True

        if not (self.use_password or self.token):
            raise NotAuthenticatedError("Insufficient credentials")

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
