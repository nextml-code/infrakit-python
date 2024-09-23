import json
from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel

from .auth import Auth
from .project import (
    CoordinateSystem,
    HeightSystem,
    Organization,
    Project,
    ProjectCreationResponse,
)


class Projects(BaseModel):
    auth: Auth

    def list(
        self,
        organizationProjects: Optional[bool] = False,
        organizationUuid: Optional[str] = None,
    ) -> List[Project]:
        url = f"{self.auth.base_url()}/projects"

        params = {}
        if organizationProjects:
            params["organizationProjects"] = organizationProjects
        if organizationUuid:
            params["organizationUuid"] = organizationUuid

        projects_data = self.auth.get(url, params=params)
        return [
            Project(
                id=project_data["id"],
                uuid=project_data["uuid"],
                name=project_data["name"],
                timestamp=project_data["timestamp"],
                archived=project_data["archived"],
                reportsEnabled=project_data["reportsEnabled"],
                organization=Organization(**project_data.get("organization", {})),
                coordinateSystem=CoordinateSystem(
                    **project_data.get("coordinateSystem", {})
                ),
                heightSystem=HeightSystem(**project_data.get("heightSystem", {})),
                auth=self.auth,
            )
            for project_data in projects_data
        ]

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
    ) -> ProjectCreationResponse:
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

        url = f"{self.auth.base_url()}/project"

        response_data = self.auth.post(url, json=project_data)
        assert response_data["status"] is True

        return ProjectCreationResponse(**response_data)
