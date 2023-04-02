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


def test_parse_returns_dict_when_status_code_200():
    # Arrange
    response = Mock(status_code=200, headers={"Content-Type": "application/json"})
    response.json.return_value = {"key": "value"}
    parser = BaseClient()

    # Act
    result = parser.parse(response)

    # Assert
    assert result == {"key": "value"}


def test_parse_returns_none_when_status_code_204():
    # Arrange
    response = Mock(status_code=204, headers={"Content-Type": "application/json"})
    parser = BaseClient()

    # Act
    result = parser.parse(response)

    # Assert
    assert result is None


def test_parse_raises_InvalidIDError_when_status_code_400():
    # Arrange
    response = Mock(status_code=400, headers={"Content-Type": "application/json"})
    response.json.return_value = {"error": {"message": "Invalid ID"}}

    parser = BaseClient()

    # Act/Assert
    with pytest.raises(InvalidIDError, match="Invalid ID"):
        parser.parse(response)


def test_parse_raises_NotAuthenticatedError_when_status_code_401():
    # Arrange
    response = Mock(
        status_code=401,
        headers={"Content-Type": "application/json"},
    )
    response.json.return_value = {"error": {"message": "Not authenticated"}}
    parser = BaseClient()

    # Act/Assert
    with pytest.raises(NotAuthenticatedError, match="Not authenticated"):
        parser.parse(response)


def test_parse_raises_NotFoundIDError_when_status_code_404():
    # Arrange
    response = Mock(
        status_code=404,
        headers={"Content-Type": "application/json"},
    )
    response.json.return_value = {"error": {"message": "ID not found"}}
    parser = BaseClient()

    # Act/Assert
    with pytest.raises(NotFoundIDError, match="ID not found"):
        parser.parse(response)


def test_parse_raises_PermissionError_when_status_code_403():
    # Arrange
    response = Mock(
        status_code=403,
        headers={"Content-Type": "application/json"},
    )
    response.json.return_value = {"error": {"message": "Permission denied"}}
    parser = BaseClient()

    # Act/Assert
    with pytest.raises(PermissionError, match="Permission denied"):
        parser.parse(response)


def test_parse_raises_UnknownError_when_status_code_is_not_handled():
    # Arrange
    response = Mock(
        status_code=500,
        headers={"Content-Type": "application/json"},
    )
    response.json.return_value = {"error": {"message": "Unknown error"}}
    parser = BaseClient()

    # Act/Assert
    with pytest.raises(UnknownError, match="Unknown error"):
        parser.parse(response)


# Add more test cases for other status codes and scenarios
