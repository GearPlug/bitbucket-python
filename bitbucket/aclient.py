import typing
import httpx

from .base import BaseClient


class Client(BaseClient):
    """
    A client for the BitBucket API that has to be used as an async context manager.

    Args:
        user (str): The username to use for authentication.
        password (str): The password to use for authentication.
        owner (str, optional): The name of the BitBucket account to use. If not
            specified, the authenticated user will be used.

    Example usage:
    ```
    async with Client('myusername', 'mypassword', 'myaccount') as client:
        response = await client.get_user()
        print(response)
    ```
    """

    async def __aenter__(self):
        self._session = httpx.AsyncClient(
            auth=(
                self.user,
                self.password,
            )
        )

        user_data = await self.get_user()

        # for shared repo, set baseURL to owner
        if self.username is None and user_data is not None:
            self.username = user_data.get("username")

        return self

    async def __aexit__(
        self,
        exc_type,
        exc_value,
        traceback,
    ) -> None:
        await self._session.aclose()

    async def all_pages(
        self,
        method: typing.Callable[
            ...,
            typing.Awaitable[typing.Union[typing.Dict[str, typing.Any], None]],
        ],
        *args,
        **kwargs
    ) -> typing.AsyncGenerator[typing.Dict[str, typing.Any], None]:
        """
        Retrieves all pages from a BitBucket API list endpoint and yields a generator for the items in the
        response.

        Example:

        ```python
        async for item in client.all_pages(
                client.get_issues,
                "{726f1aab-826f-4c08-a127-1224347b3d09}"
        ):
            print(item["id"])
        ```

        Args:
            method: A client class method to retrieve all pages from.
            *args: Variable length argument list to be passed to the `method` callable.
            **kwargs: Arbitrary keyword arguments to be passed to the `method` callable.

        Returns:
            An asynchronous generator that yields a dictionary of item data for each item in the response.

        Raises:
            Any exceptions raised by the `method` callable.
        """
        resp = await method(*args, **kwargs)
        while True:
            if resp is None:
                break

            for v in resp["values"]:
                yield v

            if "next" not in resp:
                break
            resp = await self._get(resp["next"])

    async def get_user(self, params=None):
        """
        Retrieves information about the current user.

        Args:
            params (dict, optional): A dictionary of query parameters to include
                in the request.

        Returns:
            A dictionary that contains information about the user, as returned
            by the BitBucket API.
        """
        return await self._get("2.0/user", params=params)

    async def get_repositories(self, params=None):
        """
        Retrieves a paginated list of all repositories owned by the workspace.

        Args:
            params (dict, optional): A dictionary of query parameters to include
                in the request.

        Returns:
            A dictionary that contains a paginated list of all repositories owned by the workspace.
        """
        return await self._get(
            "2.0/repositories/{}".format(self.username), params=params
        )

    async def get_repository(self, repository_slug, params=None):
        """
        Retrieves information about a specific repository.

        Args:
            repository_slug (str): The slug of the repository to retrieve information for.
            params (dict, optional): A dictionary of query parameters to include in the request.

        Returns:
            A dictionary containing information about the specified repository, as returned by the BitBucket API.
        """
        return await self._get(
            "2.0/repositories/{}/{}".format(self.username, repository_slug),
            params=params,
        )

    async def create_repository(self, params=None, data=None, name=None, team=None):
        """
        Creates a new repository.

        Example data:
        ```json
        {
            "scm": "git",
            "project": {
                "key": "MARS"
            }
        }
        ```

        Args:
            params (dict, optional): A dictionary of query parameters to include in the request.
            data (dict, optional): A dictionary of data to include in the request body
            name (str): The name of the new repository.
            team (str): The team that the new repository should be created under.

        Returns:
            A dictionary containing information about the newly created repository, as returned by the BitBucket API.
        """
        return await self._post(
            "2.0/repositories/{}/{}".format(team, name), params, data
        )

    async def get_repository_branches(self, repository_slug, params=None):
        """
        Retrieves a paginated list of all open branches within the specified repository.

        Args:
            repository_slug (str): The slug of the repository to retrieve information for.
            params (dict, optional): A dictionary of query parameters to include in the request.

        Returns:
            A dictionary containing a paginated list of all open branches within the specified repository, as returned by the BitBucket API.
        """
        return await self._get(
            "2.0/repositories/{}/{}/refs/branches".format(
                self.username, repository_slug
            ),
            params=params,
        )

    async def get_repository_tags(self, repository_slug, params=None):
        """
        Retrieves the tags in the repository.

        Args:
            repository_slug (str): The slug of the repository to retrieve branches for.
            params (dict, optional): A dictionary of query parameters to include in the request.

        Returns:
            A dictionary containing a paginated list of tags in the repository., as returned by the BitBucket API.
        """
        return await self._get(
            "2.0/repositories/{}/{}/refs/tags".format(self.username, repository_slug),
            params=params,
        )

    async def get_repository_commits(self, repository_slug, params=None):
        """
        Retrieves a paginated list of commits for a specific repository.

        Args:
            repository_slug (str): The slug of the repository to retrieve commits for.
            params (dict, optional): A dictionary of query parameters to include in the request.

        Returns:
            A dictionary containing information about the commits for the specified repository, as returned by the BitBucket API.
        """
        return await self._get(
            "2.0/repositories/{}/{}/commits".format(self.username, repository_slug),
            params=params,
        )

    async def get_repository_components(self, repository_slug, params=None):
        """
        Returns the components that have been defined in the issue tracker.

        Args:
            repository_slug (str): The slug of the repository to retrieve components for.
            params (dict, optional): A dictionary of query parameters to include in the request.

        Returns:
            A dictionary containing information about the components that have been defined in the issue tracker, as returned by the BitBucket API.
        """
        return await self._get(
            "2.0/repositories/{}/{}/components".format(self.username, repository_slug),
            params=params,
        )

    async def get_repository_milestones(self, repository_slug, params=None):
        """
        Retrieves the milestones that have been defined in the issue tracker.

        Args:
            repository_slug (str): The slug of the repository to retrieve milestones for.
            params (dict, optional): A dictionary of query parameters to include in the request.

        Returns:
            A dictionary containing information about the milestones that have been defined in the issue tracker, as returned by the BitBucket API.
        """
        return await self._get(
            "2.0/repositories/{}/{}/milestones".format(self.username, repository_slug),
            params=params,
        )

    async def get_repository_versions(self, repository_slug, params=None):
        """
        Retrieves the versions that have been defined in the issue tracker.

        Args:
            repository_slug (str): The slug of the repository to retrieve versions for.
            params (dict, optional): A dictionary of query parameters to include in the request.

        Returns:
            A dictionary containing information about the versions that have been defined in the issue tracker, as returned by the BitBucket API.
        """
        return await self._get(
            "2.0/repositories/{}/{}/versions".format(self.username, repository_slug),
            params=params,
        )

    async def get_repository_source_code(self, repository_slug, params=None):
        """
        Retrieves the directory listing of the root directory on the main branch.

        Args:
            repository_slug (str): The slug of the repository.
            params (dict, optional): A dictionary of query parameters to include in the request.

        Returns:
            A dictionary containing the directory listing of the root directory on the main branch, as returned by the BitBucket API.
        """
        return await self._get(
            "2.0/repositories/{}/{}/src".format(self.username, repository_slug),
            params=params,
        )

    async def get_repository_commit_path_source_code(
        self, repository_slug, commit_hash, path, params=None
    ):
        """
        Retrieves the contents of a single file, or the contents of a directory at a specified revision.

        Args:
            repository_slug (str): The slug of the repository to retrieve source code for.
            commit_hash (str): The hash of the commit to retrieve source code for.
            path (str): The path of the file or directory to retrieve source code for.
            params (dict, optional): A dictionary of query parameters to include in the request.

        Returns:
            When `path` points to a file, this endpoint returns the raw contents.
            When `path` points to a directory instead of a file, the response is a paginated list of directory and file objects.
        """
        return await self._get(
            "2.0/repositories/{}/{}/src/{}/{}".format(
                self.username, repository_slug, commit_hash, path
            ),
            params=params,
        )

    async def create_issue(self, repository_slug, data, params=None):
        """
        Creates a new issue in the specified repository.

        Args:
            repository_slug (str): The slug of the repository to create the issue in.
            data (dict): A dictionary of data to include in the request body, which must include the "title" field at a minimum.
            params (dict, optional): A dictionary of query parameters to include in the request.

        Returns:
            A dictionary containing information about the newly created issue, as returned by the BitBucket API.
        """
        return await self._post(
            "2.0/repositories/{}/{}/issues".format(self.username, repository_slug),
            data=data,
            params=params,
        )

    async def get_issue(self, repository_slug, issue_id, params=None):
        """
        Retrieves information about a specific issue in the specified repository.

        Args:
            repository_slug (str): The slug of the repository to retrieve the issue from.
            issue_id (int): The ID of the issue to retrieve.
            params (dict, optional): A dictionary of query parameters to include in the request.

        Returns:
            A dictionary containing information about the specified issue, as returned by the BitBucket API.
        """
        return await self._get(
            "2.0/repositories/{}/{}/issues/{}".format(
                self.username, repository_slug, issue_id
            ),
            params=params,
        )

    async def get_issues(self, repository_slug, params=None):
        """
        Retrieves a list of issues in the specified repository.

        Args:
            repository_slug (str): The slug of the repository to retrieve issues from.
            params (dict, optional): A dictionary of query parameters to include in the request.

        Returns:
            A dictionary containing information about the issues in the specified repository, as returned by the BitBucket API.
        """
        return await self._get(
            "2.0/repositories/{}/{}/issues".format(self.username, repository_slug),
            params=params,
        )

    async def delete_issue(self, repository_slug, issue_id, params=None):
        """
        Deletes a specific issue in the specified repository.

        Args:
            repository_slug (str): The slug of the repository to delete the issue from.
            issue_id (int): The ID of the issue to delete.
            params (dict, optional): A dictionary of query parameters to include in the request.
        """
        return await self._delete(
            "2.0/repositories/{}/{}/issues/{}".format(
                self.username, repository_slug, issue_id
            ),
            params=params,
        )

    async def create_webhook(self, repository_slug, data, params=None):
        """
        Creates a new webhook for the specified repository.

        Args:
            repository_slug (str): The slug of the repository to create the webhook for.
            data (dict): A dictionary of data to include in the request body, which must include the "url" field at a minimum.
            params (dict, optional): A dictionary of query parameters to include in the request.

        Returns:
            A dictionary containing information about the newly created webhook, as returned by the BitBucket API.
        """
        return await self._post(
            "2.0/repositories/{}/{}/hooks".format(self.username, repository_slug),
            data=data,
            params=params,
        )

    async def get_webhook(self, repository_slug, webhook_uid, params=None):
        """
        Retrieves information about a specific webhook in the specified repository.

        Args:
            repository_slug (str): The slug of the repository to retrieve the webhook from.
            webhook_uid (str): The UID of the webhook to retrieve.
            params (dict, optional): A dictionary of query parameters to include in the request.

        Returns:
            A dictionary containing information about the specified webhook, as returned by the BitBucket API.
        """
        return await self._get(
            "2.0/repositories/{}/{}/hooks/{}".format(
                self.username, repository_slug, webhook_uid
            ),
            params=params,
        )

    async def get_webhooks(self, repository_slug, params=None):
        """
        Retrieves a list of webhooks in the specified repository.

        Args:
            repository_slug (str): The slug of the repository to retrieve webhooks from.
            params (dict, optional): A dictionary of query parameters to include in the request.

        Returns:
            A dictionary containing information about the webhooks in the specified repository, as returned by the BitBucket API.
        """
        return await self._get(
            "2.0/repositories/{}/{}/hooks".format(self.username, repository_slug),
            params=params,
        )

    async def delete_webhook(self, repository_slug, webhook_uid, params=None):
        """
        Deletes a specific webhook in the specified repository.

        Args:
            repository_slug (str): The slug of the repository to delete the webhook from.
            webhook_uid (str): The UID of the webhook to delete.
            params (dict, optional): A dictionary of query parameters to include in the request.
        """
        return await self._delete(
            "2.0/repositories/{}/{}/hooks/{}".format(
                self.username, repository_slug, webhook_uid
            ),
            params=params,
        )

    async def _get(self, endpoint, params=None):
        """
        Sends a GET request to the specified endpoint and returns the parsed response.

        Args:
            endpoint (str): The endpoint to send the GET request to.
            params (dict, optional): A dictionary of query parameters to include in the request.

        Returns:
            A dictionary containing the parsed response from the GET request.
        """
        response = await self._session.get(
            endpoint if endpoint.startswith("http") else self.BASE_URL + endpoint,
            params=params,
        )
        return self.parse(response)

    async def _post(self, endpoint, params=None, data=None):
        """
        Sends a POST request to the specified endpoint with the specified data and returns the parsed response.

        Args:
            endpoint (str): The endpoint to send the POST request to.
            params (dict, optional): A dictionary of query parameters to include in the request.
            data (dict, optional): A dictionary of data to include in the request body.

        Returns:
            A dictionary containing the parsed response from the POST request.
        """
        response = await self._session.post(
            self.BASE_URL + endpoint,
            params=params,
            json=data,
        )
        return self.parse(response)

    async def _put(self, endpoint, params=None, data=None):
        """
        Sends a PUT request to the specified endpoint with the specified data and returns the parsed response.

        Args:
            endpoint (str): The endpoint to send the PUT request to.
            params (dict, optional): A dictionary of query parameters to include in the request.
            data (dict, optional): A dictionary of data to include in the request body.

        Returns:
            A dictionary containing the parsed response from the PUT request.
        """
        response = await self._session.put(
            self.BASE_URL + endpoint,
            params=params,
            json=data,
        )
        return self.parse(response)

    async def _delete(self, endpoint, params=None):
        """
        Sends a DELETE request to the specified endpoint with the specified data and returns the parsed response.

        Args:
            endpoint (str): The endpoint to send the DELETE request to.
            params (dict, optional): A dictionary of query parameters to include in the request.
            data (dict, optional): A dictionary of data to include in the request body.

        Returns:
            A dictionary containing the parsed response from the DELETE request.
        """
        response = await self._session.delete(self.BASE_URL + endpoint, params=params)
        return self.parse(response)
