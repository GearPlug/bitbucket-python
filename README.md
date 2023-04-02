bitbucket-python is an API wrapper for Bitbucket written in Python

## Installing
```
pip install bitbucket-python
```

## Usage

```python
from bitbucket.client import Client
from bitbucket import AsyncClient

client = Client('EMAIL', 'PASSWORD')

# Or to specify owner URL to find repo own by other user
client = Client('EMAIL', 'PASSWORD', 'Owner')

# Async client
async with AsyncClient('EMAIL', 'PASSWORD') as client:
    ...

```

### Methods

Get user information
```
response = client.get_user()
```

Get account privileges for repositories
```
response = client.get_privileges()
```

Get repositories
```
response = client.get_repositories()
```

Get repository
```
response = client.get_repository('REPOSITORY_SLUG')
```

Post repository
```
response = client.create_repository(data, params, repositoryName, teamName)
```

Get branches for repository
```
response = client.get_repository_branches('REPOSITORY_SLUG')
```

Get tags for repository
```
response = client.get_repository_tags('REPOSITORY_SLUG')
```

Get commits for a repository
```
response = client.get_repository_commits('REPOSITORY_SLUG')
```

Get components for repository
```
response = client.get_repository_components('REPOSITORY_SLUG')
```

Get milestones for repository
```
response = client.get_repository_milestones('REPOSITORY_SLUG')
```

Get versions for repository
```
response = client.get_repository_versions('REPOSITORY_SLUG')
```

Create issue
```
data = {..DATA..}
response = client.create_issue('REPOSITORY_SLUG', data)
```

Get all issues
```
response = client.get_issues('REPOSITORY_SLUG')
```

Get issue
```
response = client.get_issue('REPOSITORY_SLUG', 'ISSUE_ID')
```

Delete issue
```
response = client.delete_issue('REPOSITORY_SLUG', 'ISSUE_ID')
```

### Webhooks

Create webhook
```
data = {
    "description": "Webhook",
    "url": "http://mywebsite.com",
    "active": True,
    "events": [
        "repo:push",
        "issue:created",
        "issue:updated"
    ]
}
response = client.create_webhook('REPOSITORY_SLUG', data)
```

Get all webhooks
```
response = client.get_webhooks('REPOSITORY_SLUG')
```

Get webhook
```
response = client.get_webhook('REPOSITORY_SLUG', 'WEBHOOK_ID')
```

Delete webhook
```
response = client.delete_webhook('REPOSITORY_SLUG', 'WEBHOOK_ID')
```

### Helper methods

### all_pages

The `all_pages` method is a helper function that makes it easy to retrieve all items from an API methods that uses pagination (see https://developer.atlassian.com/cloud/bitbucket/rest/intro/#pagination).

```python
client = Client()

items = list(client.all_pages(client.get_repositories))
```

Note that the `all_pages` method uses a generator to return the results.


## Requirements

- requests
- [httpx](https://github.com/encode/httpx/)
