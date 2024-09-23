import json
from datetime import datetime
from typing import Any, Dict, List, Optional

import requests
from pydantic import BaseModel
from requests.exceptions import HTTPError

from .auth import Auth


class CoordinateSystem(BaseModel):
    name: str
    identifier: str
    projString: str
    wgs84Parameters: str
    offsetN: float
    offsetE: float
    country: str
    visible: bool


class HeightSystem(BaseModel):
    name: str
    identifier: str
    country: str
    visible: bool


class AccuracyTolerance(BaseModel):
    x: float
    y: float
    z: float
    enabled: bool


class ProjectData(BaseModel):
    name: str
    coordinateSystem: CoordinateSystem
    heightSystem: HeightSystem
    crossSectionWidth: float
    crossSectionYScale: float
    crossSectionLogpointDelta: float
    endDate: datetime
    hidden: bool
    accuracyTolerance: AccuracyTolerance
    optLock: int
    reportsEnabled: bool
    truckMode: int


class Projects(BaseModel):
    auth: Auth

    def list(self) -> List[dict]:
        url = f"{self.auth.base_url()}/projects"
        headers = self.auth.auth_headers()

        response = requests.get(url, headers=headers)
        response.raise_for_status()

        return response.json()

    def create(
        self,
        name: str,
        coordinate_system: Optional[Dict[str, Any]] = None,
        height_system: Optional[Dict[str, Any]] = None,
        cross_section_width: Optional[float] = None,
        cross_section_y_scale: Optional[float] = None,
        cross_section_logpoint_delta: Optional[float] = None,
        end_date: Optional[datetime] = None,
        hidden: Optional[bool] = None,
        accuracy_tolerance: Optional[Dict[str, Any]] = None,
        opt_lock: Optional[int] = None,
        reports_enabled: Optional[bool] = None,
        truck_mode: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Create a new project in Infrakit.

        Args:
            name (str): The name of the project. This is the only mandatory field.
            coordinate_system (Optional[Dict[str, Any]]): The coordinate system for the project. If omitted, a default system will be assigned.
            height_system (Optional[Dict[str, Any]]): The height system for the project. If omitted, a default system will be assigned.
            cross_section_width (Optional[float]): The width of the cross section.
            cross_section_y_scale (Optional[float]): The Y-scale of the cross section.
            cross_section_logpoint_delta (Optional[float]): The logpoint delta for the cross section.
            end_date (Optional[datetime]): The end date of the project.
            hidden (Optional[bool]): Whether the project is hidden.
            accuracy_tolerance (Optional[Dict[str, Any]]): The accuracy tolerance settings for the project.
            opt_lock (Optional[int]): The optimistic locking value.
            reports_enabled (Optional[bool]): Whether reports are enabled for the project.
            truck_mode (Optional[int]): The truck mode setting for the project.

        Returns:
            Dict[str, Any]: The created project data as returned by the Infrakit API.

        Raises:
            requests.HTTPError: If the API request fails.

        Note:
            All fields except 'name' are optional and have default values if omitted.
            The coordinate system and height system will be assigned default values if not provided.
        """
        project_data = {"name": name}

        if coordinate_system is not None:
            project_data["coordinateSystem"] = coordinate_system
        if height_system is not None:
            project_data["heightSystem"] = height_system
        if cross_section_width is not None:
            project_data["crossSectionWidth"] = cross_section_width
        if cross_section_y_scale is not None:
            project_data["crossSectionYScale"] = cross_section_y_scale
        if cross_section_logpoint_delta is not None:
            project_data["crossSectionLogpointDelta"] = cross_section_logpoint_delta
        if end_date is not None:
            project_data["endDate"] = end_date.isoformat()
        if hidden is not None:
            project_data["hidden"] = hidden
        if accuracy_tolerance is not None:
            project_data["accuracyTolerance"] = accuracy_tolerance
        if opt_lock is not None:
            project_data["optLock"] = opt_lock
        if reports_enabled is not None:
            project_data["reportsEnabled"] = reports_enabled
        if truck_mode is not None:
            project_data["truckMode"] = truck_mode

        url = f"{self.auth.base_url()}/projects"
        headers = self.auth.auth_headers()
        headers["Content-Type"] = "application/json"  # Add this line

        print(f"Request URL: {url}")
        print(f"Request Headers: {headers}")
        print(f"Request Payload: {json.dumps(project_data, indent=2)}")

        try:
            response = requests.post(url, json=project_data, headers=headers)
            print(f"Response Status Code: {response.status_code}")
            print(f"Response Headers: {response.headers}")
            print(f"Response Text: {response.text}")
            response.raise_for_status()
            return response.json()
        except HTTPError as http_err:
            error_message = f"HTTP error occurred: {http_err}"
            try:
                error_detail = response.json()
                error_message += (
                    f"\nAPI Error Details: {json.dumps(error_detail, indent=2)}"
                )
            except json.JSONDecodeError:
                error_message += f"\nAPI Response Text: {response.text}"

            error_message += f"\nRequest Payload: {json.dumps(project_data, indent=2)}"
            raise HTTPError(error_message) from http_err
        except Exception as err:
            raise Exception(f"An error occurred: {err}") from err
