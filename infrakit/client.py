from __future__ import annotations

from pydantic import BaseModel

from .auth import Auth
from .projects import Projects


class InfrakitClient(BaseModel):
    auth: Auth

    @classmethod
    def from_credentials(
        cls,
        username: str,
        password: str,
        mode: str = "production",
    ) -> InfrakitClient:
        return cls(auth=Auth(username=username, password=password, mode=mode))

    @classmethod
    def from_env(cls) -> InfrakitClient:
        return cls(auth=Auth.from_env())

    @classmethod
    def from_env_file(cls, path: str) -> InfrakitClient:
        return cls(auth=Auth.from_env_file(path))

    @property
    def projects(self) -> Projects:
        return Projects(auth=self.auth)
