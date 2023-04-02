from unittest.mock import MagicMock, Mock, call, patch
import pytest

from bitbucket.client import Client


class TestClient:
    @pytest.fixture
    def client(self):
        return Client("", "", "")

    def test_no_pages(self, client):
        method = lambda: None
        result = list(client.all_pages(method))
        assert result == []

    def test_single_page(self, client):
        method = lambda: {"values": [{"id": 1}, {"id": 2}, {"id": 3}]}
        result = list(client.all_pages(method))
        assert result == [{"id": 1}, {"id": 2}, {"id": 3}]

    def test_multiple_pages(self, client):
        method = lambda: {"values": [{"id": 1}, {"id": 2}], "next": "/api?page=2"}

        get_mock = MagicMock(
            side_effect=[
                {"values": [{"id": 3}, {"id": 4}], "next": "/api?page=3"},
                {"values": [{"id": 5}, {"id": 6}]},
            ]
        )
        client._get = get_mock
        result = list(client.all_pages(method))
        expected = [{"id": 1}, {"id": 2}, {"id": 3}, {"id": 4}, {"id": 5}, {"id": 6}]

        assert result == expected
        assert get_mock.call_count == 2
        assert get_mock.call_args_list[0] == call(
            "/api?page=2",
        )
        assert get_mock.call_args_list[1] == call(
            "/api?page=3",
        )
