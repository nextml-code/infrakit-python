# infrakit-python

Unofficial Infrakit API client for python.

## Installation

```bash
poetry add infrakit
```

## Usage

```python
import infrakit

client = infrakit.Client.from_env()

project = client.projects.list()[0]
```

## Development

```bash
poetry install
```

```bash
poetry run pytest -s
```

API docs: https://docs.infrakit.com/

Integration manual: https://support.infrakit.com/help/integration-manual-for-infrakit-api

## Environment Variables
- `USERNAME`: Your Infrakit username (should be the entire email)
- `PASSWORD`: Your Infrakit password
- `MODE`: The mode of the environment (production, beta, development, test)

## Example Usage
```python
from infrakit.client import InfrakitClient

client = InfrakitClient.from_env()
print(client.projects.list())
```

````

These changes will log the response details, which should help us understand what might be going wrong with the request.
