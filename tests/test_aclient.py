from unittest.mock import MagicMock, call
import pytest

from bitbucket import AsyncClient


class AsyncMock(MagicMock):
    async def __call__(self, *args, **kwargs):
        return super(AsyncMock, self).__call__(*args, **kwargs)


class TestAsyncClient:
    @pytest.fixture
    def client(self):
        return AsyncClient("", "", "")

    @pytest.mark.asyncio
    async def test_no_pages(self, client):
        async def method(params):
            return None

        result = [x async for x in client.all_pages(method, {})]
        assert result == []

    @pytest.mark.asyncio
    async def test_single_page(self, client):
        async def method(params):
            return {"values": [{"id": 1}, {"id": 2}, {"id": 3}]}

        result = [x async for x in client.all_pages(method, {})]
        assert result == [{"id": 1}, {"id": 2}, {"id": 3}]

    @pytest.mark.asyncio
    async def test_multiple_pages(self, client):
        async def method(params):
            return {"values": [{"id": 1}, {"id": 2}], "next": "/api?page=2"}

        get_mock = AsyncMock(
            side_effect=[
                {"values": [{"id": 3}, {"id": 4}], "next": "/api?page=3"},
                {"values": [{"id": 5}, {"id": 6}]},
            ]
        )
        client._get = get_mock
        result = [x async for x in client.all_pages(method, {})]
        expected = [{"id": 1}, {"id": 2}, {"id": 3}, {"id": 4}, {"id": 5}, {"id": 6}]
        assert result == expected
        assert get_mock.call_count == 2
        assert get_mock.call_args_list[0] == call(
            "/api?page=2",
        )
        assert get_mock.call_args_list[1] == call(
            "/api?page=3",
        )
