import json
from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel

from .auth import Auth


class Organization(BaseModel):
    uuid: Optional[str] = None
    name: Optional[str] = None


class CoordinateSystem(BaseModel):
    name: Optional[str] = None
    identifier: Optional[str] = None
    projString: Optional[str] = None
    wgs84Parameters: Optional[str] = None
    offsetN: Optional[float] = None
    offsetE: Optional[float] = None
    country: Optional[str] = None
    visible: Optional[bool] = None


class HeightSystem(BaseModel):
    name: Optional[str] = None
    identifier: Optional[str] = None
    country: Optional[str] = None
    visible: Optional[bool] = None


class Project(BaseModel):
    id: int
    uuid: str
    name: str
    timestamp: int
    archived: bool
    reportsEnabled: bool
    organization: Optional[Organization] = None
    coordinateSystem: Optional[CoordinateSystem] = None
    heightSystem: Optional[HeightSystem] = None
    auth: Auth

    def folders(self, depth: int = 0) -> Dict[str, Any]:
        url = f"{self.auth.base_url()}/project/{self.uuid}/folders?depth={depth}"
        return self.auth.get(url)


class ProjectCreationResponse(BaseModel):
    status: bool
    uuid: str
    id: int
