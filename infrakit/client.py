from __future__ import annotations

import json
from typing import Generator, List, Optional

import requests
from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic_settings import BaseSettings


class InfrakitClient(BaseModel):
    customer_id: str
    subdomain: Optional[str] = None
    client_id: str
    client_secret: str

    @classmethod
    def from_env(cls) -> InfrakitClient:

        class Settings(BaseSettings):
            customer_id: str
            subdomain: Optional[str] = None
            client_id: str
            client_secret: str

        settings = Settings()

        return cls(
            customer_id=settings.customer_id,
            subdomain=settings.subdomain,
            client_id=settings.client_id,
            client_secret=settings.client_secret,
        )

    @classmethod
    def from_env_file(cls, path: str) -> InfrakitClient:
        load_dotenv(path)
        return cls.from_env()

    def base_url(self) -> str:
        if self.subdomain is None:
            subdomain = self.customer_id
        else:
            subdomain = self.subdomain
        return f"https://{subdomain}.api.infrakit.com/api/v1"

    def auth_headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.access_token()}",
            "X-Customer-ID": self.customer_id,
        }

    def openid_connect_url(self) -> str:
        return f"https://auth.infrakit.com/auth/realms/{self.customer_id}/.well-known/openid-configuration"

    def access_token(self) -> str:
        response = requests.get(self.openid_connect_url())
        if response.status_code != 200:
            raise Exception("Failed to authenticate with OIDC")

        oidc_discoveries = response.json()
        token_url = oidc_discoveries["token_endpoint"]

        response = requests.post(
            token_url,
            data=dict(grant_type="client_credentials"),
            auth=(self.client_id, self.client_secret),
        )

        if response.status_code != 200:
            raise Exception(
                f"Failed to authenticate, status code {response.status_code}, text {response.text}"
            )

        return response.json()["access_token"]

    @property
    def alerts(self) -> Alerts:
        return Alerts(client=self)


class Alerts(BaseModel):
    client: InfrakitClient

    def list(self) -> List[dict]:
        url = f"{self.client.base_url()}/alerts"
        response = requests.get(url, headers=self.client.auth_headers())
        response.raise_for_status()
        return response.json()

    def post(self, alert: dict) -> dict:
        url = f"{self.client.base_url()}/alert"
        response = requests.post(url, json=alert, headers=self.client.auth_headers())
        response.raise_for_status()
        return response.json()
