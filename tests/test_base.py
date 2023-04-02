from unittest.mock import Mock

import pytest

from bitbucket.base import BaseClient
from bitbucket.exceptions import (
    InvalidIDError,
    NotAuthenticatedError,
    NotFoundIDError,
    PermissionError,
    UnknownError,
)


class TestBaseClient:
    @pytest.fixture
    def client(self):
        return BaseClient("", "")

    def test_parse_returns_dict_when_status_code_200(self, client):
        # Arrange
        response = Mock(status_code=200, headers={"Content-Type": "application/json"})
        response.json.return_value = {"key": "value"}

        # Act
        result = client.parse(response)

        # Assert
        assert result == {"key": "value"}

    def test_parse_returns_none_when_status_code_204(self, client):
        # Arrange
        response = Mock(status_code=204, headers={"Content-Type": "application/json"})

        # Act
        result = client.parse(response)

        # Assert
        assert result is None

    def test_parse_raises_InvalidIDError_when_status_code_400(self, client):
        # Arrange
        response = Mock(status_code=400, headers={"Content-Type": "application/json"})
        response.json.return_value = {"error": {"message": "Invalid ID"}}

        # Act/Assert
        with pytest.raises(InvalidIDError, match="Invalid ID"):
            client.parse(response)

    def test_parse_raises_NotAuthenticatedError_when_status_code_401(self, client):
        # Arrange
        response = Mock(
            status_code=401,
            headers={"Content-Type": "application/json"},
        )
        response.json.return_value = {"error": {"message": "Not authenticated"}}

        # Act/Assert
        with pytest.raises(NotAuthenticatedError, match="Not authenticated"):
            client.parse(response)

    def test_parse_raises_NotFoundIDError_when_status_code_404(self, client):
        # Arrange
        response = Mock(
            status_code=404,
            headers={"Content-Type": "application/json"},
        )
        response.json.return_value = {"error": {"message": "ID not found"}}

        # Act/Assert
        with pytest.raises(NotFoundIDError, match="ID not found"):
            client.parse(response)

    def test_parse_raises_PermissionError_when_status_code_403(self, client):
        # Arrange
        response = Mock(
            status_code=403,
            headers={"Content-Type": "application/json"},
        )
        response.json.return_value = {"error": {"message": "Permission denied"}}

        # Act/Assert
        with pytest.raises(PermissionError, match="Permission denied"):
            client.parse(response)

    def test_parse_raises_UnknownError_when_status_code_is_not_handled(self, client):
        # Arrange
        response = Mock(
            status_code=500,
            headers={"Content-Type": "application/json"},
        )
        response.json.return_value = {"error": {"message": "Unknown error"}}

        # Act/Assert
        with pytest.raises(UnknownError, match="Unknown error"):
            client.parse(response)


# Add more test cases for other status codes and scenarios
