from __future__ import annotations

import json
import os
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
    def from_env(cls, path: Optional[str] = None):

        if path is not None:
            load_dotenv(path)

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

    def base_url(self):
        if self.subdomain is None:
            subdomain = self.customer_id
        else:
            subdomain = self.subdomain
        return f"https://{subdomain}.api.track.deepinspection.io/external/v0-alpha"

    def auth_headers(self):
        return {
            "Authorization": f"Bearer {self.access_token()}",
            "X-Customer-ID": self.customer_id,
        }

    def openid_connect_url(self):
        return f"https://auth.nextml.com/auth/realms/deepinspection-track-{self.customer_id}/.well-known/openid-configuration"

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

    def list(self) -> List[dict]:
        url = f"{self.base_url()}/exports/fastenings"
        response = requests.get(url, headers=self.auth_headers())
        response.raise_for_status()
        return response.json()

    def get(self, export_id) -> dict:
        url = f"{self.base_url()}/exports/fastenings/{export_id}"
        response = requests.get(url, headers=self.auth_headers())
        response.raise_for_status()
        return response.json()

    def get_data(self, export_id) -> Generator[dict, None, None]:
        url = f"{self.base_url()}/exports/fastenings/{export_id}/data"
        response = requests.get(
            url,
            headers={
                **self.auth_headers(),
                "Accept": "application/x-ndjson",
            },
            stream=True,
        )
        response.raise_for_status()

        for line in response.iter_lines():
            if line:
                yield json.loads(line.decode("utf-8"))
