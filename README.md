bitbucket-python is an API wrapper for Bitbucket written in Python

## Installing
```
pip install bitbucket-python
```

## Usage
```
from bitbucket.client import Client

client = Client('EMAIL', 'PASSWORD')
```

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

Get branches for repository
```
response = client.get_repository_branches('REPOSITORY_SLUG')
```

Get tags for repository
```
response = client.get_repository_tags('REPOSITORY_SLUG')
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

## Requirements
- requests
