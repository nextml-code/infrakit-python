import json
from typing import Any, Dict, Optional

from pydantic import BaseModel
from requests.exceptions import HTTPError

from .auth import Auth


class FolderData(BaseModel):
    name: str
    parentUuid: Optional[str] = None


class Folder(BaseModel):
    auth: Auth

    def get(self, folder_id: str) -> Dict[str, Any]:
        url = f"{self.auth.base_url()}/folder/{folder_id}"
        return self.auth.get(url)

    def create(self, name: str, parentUuid: str) -> Dict[str, Any]:
        folder_data = {"name": name, "parentUuid": parentUuid}

        return self.auth.post(f"{self.auth.base_url()}/folder", params=folder_data)
