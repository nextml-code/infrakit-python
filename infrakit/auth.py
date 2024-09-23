from __future__ import annotations

import json
from typing import Optional

import requests
from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic_settings import BaseSettings
from requests.exceptions import HTTPError

from .mode import Mode


class Auth(BaseModel):
    username: str
    password: str
    mode: Mode = Mode.PRODUCTION

    @classmethod
    def from_env(cls) -> Auth:

        class Settings(BaseSettings):
            username: str
            password: str
            mode: Mode = Mode.PRODUCTION

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
            "Content-Type": "application/json",
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
        if self.mode == Mode.PRODUCTION:
            return "https://app.infrakit.com/kuura/v1"
        elif self.mode == Mode.BETA:
            return "https://beta.infrakit.com/kuura/v1"
        elif self.mode == Mode.TEST:
            return "https://test.infrakit.com/kuura/v1"
        else:
            raise ValueError(f"Invalid mode: {self.mode}")

    def headers(self) -> dict:
        return {
            **self.auth_headers(),
            "Accept": "application/json",
        }

    def get(self, url: str, params: Optional[dict] = None) -> dict:
        response = requests.get(url, headers=self.headers(), params=params)
        return self._handle_response(response, url, "GET")

    def post(
        self, url: str, json: Optional[dict] = None, params: Optional[dict] = None
    ) -> dict:
        response = requests.post(url, json=json, params=params, headers=self.headers())
        return self._handle_response(response, url, "POST", json)

    def put(self, url: str, json: dict) -> dict:
        response = requests.put(url, json=json, headers=self.headers())
        return self._handle_response(response, url, "PUT", json)

    def delete(self, url: str) -> dict:
        response = requests.delete(url, headers=self.headers())
        return self._handle_response(response, url, "DELETE")

    def _handle_response(
        self, response: requests.Response, url: str, method: str, payload: dict = None
    ) -> dict:
        try:
            response.raise_for_status()
            response_data = response.json()

            # Check for 'status' field in the response
            if isinstance(response_data, dict) and not response_data.get(
                "status", True
            ):
                error_message = response_data.get("error", "Unknown error occurred")
                raise HTTPError(f"API error: {error_message}")

            return response_data
        except Exception as err:
            if isinstance(err, HTTPError):
                error_message = f"HTTP error occurred: {err}"
            elif isinstance(err, json.JSONDecodeError):
                error_message = f"Response is not in JSON format: {err}"
            else:
                error_message = f"An error occurred: {err}"
            error_message += f"\nRequest URL: {url}"
            error_message += f"\nRequest Method: {method}"
            if payload:
                error_message += f"\nRequest Payload: {json.dumps(payload, indent=2)}"

            error_message += f"\nAPI Response Text: {response.text}"

            raise HTTPError(error_message) from err
