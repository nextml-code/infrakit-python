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

client = infrakit.Client.from_credentials(
    username="your-email",
    password="your-password",
)

projects = client.projects.list()

project = projects[0]

folders = project.folders()

client.document.create(
    name="Test Document",
    url="https://www.google.com",
    projectId=project.id,
    folderUuid=folders[0]["uuid"],
    description="",
    geographicPoint=GeographicPoint(
        lat=50.0, lon=14.0, elevation=0.0
    ),
)
```

## Development

.env.secrets:

```bash
USERNAME=your-email
PASSWORD=your-password
MODE=production
```

```bash
poetry install
```

Run tests:

```bash
poetry run pytest -s
```
