from datetime import datetime, timedelta

import pytest
from requests.exceptions import HTTPError

from infrakit.client import InfrakitClient
from infrakit.project import Project, ProjectCreationResponse


@pytest.fixture
def client():
    return InfrakitClient.from_env_file(".env.secrets")


def test_list_projects(client: InfrakitClient):
    projects = client.projects.list()
    print(projects)
    assert isinstance(projects, list)
    assert all(isinstance(project, Project) for project in projects)


def test_create_project(client: InfrakitClient):
    # Generate a unique project name using the current timestamp
    project_name = f"Test Project {datetime.now().isoformat()}"

    try:
        # Create a project with minimal required information
        new_project = client.projects.create(
            name=project_name,
            end_date=datetime.now()
            + timedelta(days=30),  # Set end date to 30 days from now
        )

        assert isinstance(new_project, ProjectCreationResponse)

        # Verify that the project was created by listing all projects
        projects = client.projects.list(organizationProjects=True)
        assert any(project.name == project_name for project in projects)
    except HTTPError as http_err:
        pytest.fail(f"Failed to create project. Error details:\n{http_err}")
    except Exception as err:
        pytest.fail(f"An unexpected error occurred: {err}")


def test_list_folders_in_project(client: InfrakitClient):
    # List existing projects and use the first one
    projects = client.projects.list()
    assert len(projects) > 0, "No projects found"
    project = projects[0]

    # List folders within the project
    folders_response = project.folders()
    print(f"Folders Response: {folders_response}")
    assert isinstance(folders_response, dict)
    assert "folders" in folders_response
    folders = folders_response["folders"]


def test_create_folder(client: InfrakitClient):

    # List existing projects and use the first one
    projects = client.projects.list()
    assert len(projects) > 0, "No projects found"
    project = projects[0]

    # List folders within the project
    folders_response = project.folders()
    print(f"Folders Response: {folders_response}")
    assert isinstance(folders_response, dict)
    assert "folders" in folders_response
    folders = folders_response["folders"]

    folder_name = f"Test Folder {datetime.now().isoformat()}"

    new_folder = client.folder.create(
        name=folder_name, parentUuid=folders_response["folders"][0]["uuid"]
    )
    print(new_folder)
    assert isinstance(new_folder, dict)

    retrieved_folder = client.folder.get(folder_id=new_folder["uuid"])
    print(retrieved_folder)
