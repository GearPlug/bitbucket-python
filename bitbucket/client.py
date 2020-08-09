import requests

from bitbucket.exceptions import UnknownError, InvalidIDError, NotFoundIDError, NotAuthenticatedError, PermissionError


class Client(object):
    BASE_URL = 'https://api.bitbucket.org/'

    def __init__(self, user:str, password:str, owner=None):        
        """Initial session with user/password, and setup repository owner 

        Args:
            params:

        Returns:

        """

        self.user = user
        self.workspace = user
        self.password = password

        user_data = self.get_user()

        # for shared repo, set baseURL to owner
        if owner is None :
            owner = user_data.get('username')
        self.username = owner

    def get_user(self, params=None):
        """Returns the currently logged in user.

        Args:
            params:

        Returns:

        """
        return self._get('2.0/user', params=params)

    def set_workspaces(self, org_name, params=None):
        """Sets the organization to which the repos belong."""
        self.workspace = org_name

    def get_privileges(self, params=None):
        """Gets a list of all the privilege across all an account's repositories.
        If a repository has no individual users with privileges, it does not appear in this list.
        Only the repository owner, a team account administrator, or an account with administrative
        rights on the repository can make this call. This method has the following parameters:


        Args:
            params:

        Returns:

        """
        return self._get('1.0/privileges/{}'.format(self.username), params=params)

    def get_repositories(self, params=None):
        """Returns a paginated list of all repositories owned by the specified account or UUID.

        The result can be narrowed down based on the authenticated user's role.

        E.g. with ?role=contributor, only those repositories that the authenticated user has write access to are
        returned (this includes any repo the user is an admin on, as that implies write access).

        This endpoint also supports filtering and sorting of the results. See filtering and sorting for more details.

        Args:
            params:

        Returns:

        """
        return self._get('2.0/repositories/{}'.format(self.username), params=params)

    def get_repository(self, repository_slug, params=None):
        """Returns the object describing this repository.

        Args:
            repository_slug:
            params:

        Returns:

        """
        return self._get('2.0/repositories/{}/{}'.format(self.username, repository_slug), params=params)

    def get_repository_pipelines(self, repository_slug, page=None, params=None):
        """Returns the object describing this repository's pipelines.

        Args:
            repository_slug:
            params:

        Returns:

        """
        page_num = str(page) if page else '1'
        return self._get('2.0/repositories/{}/{}/pipelines/?page={}'.format(self.workspace, repository_slug, page_num), params=params)

    def get_repository_branches(self, repository_slug, params=None):
        return self._get('2.0/repositories/{}/{}/refs/branches'.format(self.username, repository_slug), params=params)

    def get_repository_tags(self, repository_slug, params=None):
        return self._get('2.0/repositories/{}/{}/refs/tags'.format(self.username, repository_slug), params=params)

    def get_repository_components(self, repository_slug, params=None):
        """Returns the components that have been defined in the issue tracker.

        This resource is only available on repositories that have the issue tracker enabled.

        Args:
            repository_slug:
            params:

        Returns:

        """
        return self._get('2.0/repositories/{}/{}/components'.format(self.username, repository_slug), params=params)

    def get_repository_milestones(self, repository_slug, params=None):
        """Returns the milestones that have been defined in the issue tracker.

        This resource is only available on repositories that have the issue tracker enabled.

        Args:
            repository_slug:
            params:

        Returns:

        """
        return self._get('2.0/repositories/{}/{}/milestones'.format(self.username, repository_slug), params=params)

    def get_repository_versions(self, repository_slug, params=None):
        """Returns the versions that have been defined in the issue tracker.

        This resource is only available on repositories that have the issue tracker enabled.

        Args:
            repository_slug:
            params:

        Returns:

        """
        return self._get('2.0/repositories/{}/{}/versions'.format(self.username, repository_slug), params=params)

    def get_repository_source_code(self, repository_slug, params=None):
        """Returns data about the source code of given repository.

        Args:
            repository_slug:
            params:

        Returns:

        """
        return self._get('2.0/repositories/{}/{}/src'.format(self.username, repository_slug), params=params)

    def get_repository_commit_path_source_code(self, repository_slug, commit_hash, path, params=None):
        """Returns source code of given path at specified commit_hash of given repository.

        Args:
            repository_slug:
            commit_hash:
            path:
            params:

        Returns:

        """
        return self._get('2.0/repositories/{}/{}/src/{}/{}'.format(
            self.username,
            repository_slug,
            commit_hash,
            path
        ), params=params)

    def create_issue(self, repository_slug, title, description='', params=None):
        """Creates a new issue.

        This call requires authentication. Private repositories or private issue trackers require
        the caller to authenticate with an account that has appropriate authorisation.

        The authenticated user is used for the issue's reporter field.

        Args:
            repository_slug:
            data:
            params:

        The post data should be in the format:
            {
                "title":"title of the issue",
                "content":{
                    "raw":"this should be the description"
                }
            }

        Returns:

        """
        data = {
            "title": title,
            "content": {
                "raw": description
            }
        }
        return self._post('2.0/repositories/{}/{}/issues'.format(self.workspace, repository_slug), data=data,
                          params=params)

    def get_issue(self, repository_slug, issue_id, params=None):
        """Returns the specified issue.

        Args:
            repository_slug:
        data = {
            "title": title,
            "content": {
                "raw": description
            }
        }
        return self._post('2.0/repositories/{}/{}/issues'.format(self.workspace, repository_slug), data=data,
            params:

        Returns:

        """
        return self._get('2.0/repositories/{}/{}/issues/{}'.format(self.username, repository_slug, issue_id),
                         params=params)

    def get_issues(self, repository_slug, params=None):
        """Returns the issues in the issue tracker.

        Args:
            repository_slug:
            params:

        Returns:

        """
        return self._get('2.0/repositories/{}/{}/issues'.format(self.username, repository_slug), params=params)

    def delete_issue(self, repository_slug, issue_id, params=None):
        """Deletes the specified issue. This requires write access to the repository.

        Args:
            repository_slug:
            issue_id:
            params:

        Returns:

        """
        return self._delete('2.0/repositories/{}/{}/issues/{}'.format(self.username, repository_slug, issue_id),
                            params=params)

    def create_webhook(self, repository_slug, data, params=None):
        """Creates a new webhook on the specified repository.

        Example:
            {
              "description": "Webhook Description",
              "url": "https://example.com/",
              "active": true,
              "events": [
                "repo:push",
                "issue:created",
                "issue:updated"
              ]
            }

        Note that this call requires the webhook scope, as well as any scope that applies to the events
        that the webhook subscribes to. In the example above that means: webhook, repository and issue.
        Also note that the url must properly resolve and cannot be an internal, non-routed address.

        Args:
            repository_slug:
            data:
            params:

        Returns:

        """
        return self._post('2.0/repositories/{}/{}/hooks'.format(self.username, repository_slug), data=data,
                          params=params)

    def get_webhook(self, repository_slug, webhook_uid, params=None):
        """Returns the webhook with the specified id installed on the specified repository.

        Args:
            repository_slug:
            webhook_uid:
            params:

        Returns:

        """
        return self._get('2.0/repositories/{}/{}/hooks/{}'.format(self.username, repository_slug, webhook_uid),
                         params=params)

    def get_webhooks(self, repository_slug, params=None):
        """Returns a paginated list of webhooks installed on this repository.

        Args:
            repository_slug:
            params:

        Returns:

        """
        return self._get('2.0/repositories/{}/{}/hooks'.format(self.username, repository_slug), params=params)

    def delete_webhook(self, repository_slug, webhook_uid, params=None):
        """Deletes the specified webhook subscription from the given repository.

        Args:
            repository_slug:
            webhook_uid:
            params:

        Returns:

        """
        return self._delete('2.0/repositories/{}/{}/hooks/{}'.format(self.username, repository_slug, webhook_uid),
                            params=params)

    def _get(self, endpoint, params=None):
        response = requests.get(self.BASE_URL + endpoint, params=params, auth=(self.user, self.password))
        return self._parse(response)

    def _post(self, endpoint, params=None, data=None):
        response = requests.post(self.BASE_URL + endpoint, params=params, json=data, auth=(self.user, self.password))
        return self._parse(response)

    def _put(self, endpoint, params=None, data=None):
        response = requests.put(self.BASE_URL + endpoint, params=params, json=data, auth=(self.user, self.password))
        return self._parse(response)

    def _delete(self, endpoint, params=None):
        response = requests.delete(self.BASE_URL + endpoint, params=params, auth=(self.user, self.password))
        return self._parse(response)

    def _parse(self, response):
        status_code = response.status_code
        if 'application/json' in response.headers['Content-Type']:
            r = response.json()
        else:
            r = response.text
        if status_code in (200, 201):
            return r
        if status_code == 204:
            return None
        message = None
        try:
            if 'errorMessages' in r:
                message = r['errorMessages']
        except Exception:
            message = 'No error message.'
        if status_code == 400:
            raise InvalidIDError(message)
        if status_code == 401:
            raise NotAuthenticatedError(message)
        if status_code == 403:
            raise PermissionError(message)
        if status_code == 404:
            raise NotFoundIDError(message)
        raise UnknownError(message)
