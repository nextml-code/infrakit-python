from __future__ import annotations

import requests
from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic_settings import BaseSettings


class Auth(BaseModel):
    username: str
    password: str
    mode: str = "production"

    @classmethod
    def from_env(cls) -> Auth:

        class Settings(BaseSettings):
            username: str
            password: str
            mode: str = "production"

        settings = Settings()

        return cls(
            username=settings.username,
            password=settings.password,
            mode=settings.mode,
        )

    @classmethod
    def from_env_file(cls, path: str) -> Auth:
        load_dotenv(path, override=True)
        settings = cls.from_env()
        return settings

    def auth_headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.access_token()}",
        }

    def openid_connect_url(self) -> str:
        return f"https://iam.infrakit.com/auth/token"

    def access_token(self) -> str:
        response = requests.post(
            self.openid_connect_url(),
            data={
                "grant_type": "password",
                "username": self.username,
                "password": self.password,
            },
        )

        if response.status_code != 200:
            raise Exception(
                f"Failed to authenticate, status code {response.status_code}, text {response.text}"
            )

        return response.json()["accessToken"]

    def base_url(self) -> str:
        if self.mode == "production":
            return "https://app.infrakit.com/kuura/v1"
        elif self.mode == "beta":
            return "https://beta.infrakit.com/kuura/v1"
        elif self.mode == "development" or self.mode == "test":
            return "https://test.infrakit.com/kuura/v1"
        else:
            raise ValueError(f"Invalid mode: {self.mode}")
