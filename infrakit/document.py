from typing import Any, Dict, Optional

from pydantic import BaseModel

from .auth import Auth


class GeographicPoint(BaseModel):
    lat: float
    lon: float
    elevation: float


class Document(BaseModel):
    name: str
    url: str
    projectId: int
    folderUuid: str
    description: Optional[str] = None
    geographicPoint: Optional[GeographicPoint] = None
    auth: Auth

    def create(self) -> Dict[str, Any]:
        url = f"{self.auth.base_url()}/document/external"
        payload = {
            "name": self.name,
            "url": self.url,
            "projectId": self.projectId,
            "folderUuid": self.folderUuid,
            "description": self.description,
            "geographicPoint": (
                self.geographicPoint.model_dump() if self.geographicPoint else None
            ),
        }
        return self.auth.post(url, json=payload)
