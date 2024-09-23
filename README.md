# infrakit-python

Incomplete unofficial Infrakit python client.

_Work in progress._

- [API docs](https://docs.infrakit.com/)
- [Integration manual](https://support.infrakit.com/help/integration-manual-for-infrakit-api)

## Planned installation

```bash
poetry add infrakit
```

## Usage

```python
import infrakit

client = infrakit.Client.from_env()

project = client.projects.list()[0]
```

.env.secrets:

```bash
USERNAME=your-email
PASSWORD=your-password
MODE=production
```

## Development

```bash
poetry install
```

Run tests:

```bash
poetry run pytest -s
```
