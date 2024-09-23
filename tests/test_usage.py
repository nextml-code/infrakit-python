from datetime import datetime, timedelta

import pytest
from requests.exceptions import HTTPError

from infrakit.client import InfrakitClient


@pytest.fixture
def client():
    return InfrakitClient.from_env_file(".env.secrets")


def test_list_projects(client: InfrakitClient):
    projects = client.projects.list()
    print(projects)
    assert isinstance(projects, list)
    assert all(isinstance(project, dict) for project in projects)


# Not yet supported
# def test_create_project(client: InfrakitClient):
#     # Generate a unique project name using the current timestamp
#     project_name = f"Test Project {datetime.now().isoformat()}"

#     try:
#         # Create a project with minimal required information
#         new_project = client.projects.create(
#             name=project_name,
#             # Remove the end_date parameter for now
#         )

#         assert isinstance(new_project, dict)
#         assert new_project["name"] == project_name

#         # Verify that the project was created by listing all projects
#         projects = client.projects.list()
#         assert any(project["name"] == project_name for project in projects)
#     except HTTPError as http_err:
#         pytest.fail(f"Failed to create project. Error details:\n{http_err}")
#     except Exception as err:
#         pytest.fail(f"An unexpected error occurred: {err}")
