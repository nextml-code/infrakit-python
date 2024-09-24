from typing import Any, Dict, Optional

from pydantic import BaseModel

from .auth import Auth


class GeographicPoint(BaseModel):
    lat: float
    lon: float
    elevation: float


class Document(BaseModel):
    auth: Auth

    def create(
        self,
        name: str,
        url: str,
        projectId: int,
        folderUuid: str,
        description: Optional[str] = None,
        geographicPoint: Optional[GeographicPoint] = None,
    ) -> Dict[str, Any]:
        payload = {
            "name": name,
            "url": url,
            "projectId": projectId,
            "folderUuid": folderUuid,
            "description": description,
            "geographicPoint": geographicPoint.dict() if geographicPoint else None,
        }
        url = f"{self.auth.base_url()}/document/external"
        return self.auth.post(url, json=payload)
