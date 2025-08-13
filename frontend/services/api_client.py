from __future__ import annotations

import requests
from typing import Any, Dict, List, Optional


class ApiClient:

    def __init__(self, base_url: str = "http://localhost:8001/api/v1") -> None:
        self.base_url = base_url

    # --- helpers
    def _auth_headers(self, token: Optional[str]) -> Dict[str, str]:
        return {"Authorization": f"Bearer {token}"} if token else {}

    # --- auth
    def login(self, dni: str, password: str) -> tuple[bool, Dict[str, Any] | str]:
        try:
            response = requests.post(
                f"{self.base_url}/auth/login",
                data={"username": dni, "password": password},
                timeout=15,
            )
            if response.status_code == 200:
                return True, response.json()
            return False, response.json().get("detail", "Credenciales inválidas")
        except Exception as e:
            return False, str(e)

    def signup(self, email: str, dni: int, password: str) -> tuple[bool, Any]:
        try:
            response = requests.post(
                f"{self.base_url}/user/create",
                json={"email": email, "dni": dni, "password": password},
                timeout=15,
            )
            if response.status_code == 200:
                return True, response.json()
            return False, response.json().get("detail", "No se pudo registrar")
        except Exception as e:
            return False, str(e)

    def me(self, token: str) -> tuple[bool, Dict[str, Any] | str]:
        try:
            response = requests.get(
                f"{self.base_url}/user/me",
                headers=self._auth_headers(token),
                timeout=15,
            )
            if response.status_code == 200:
                return True, response.json()
            return False, response.text
        except Exception as e:
            return False, str(e)

    def update_user(self, token: str, first_name: str, last_name: str) -> tuple[bool, Any]:
        try:
            response = requests.post(
                f"{self.base_url}/user/update",
                headers=self._auth_headers(token),
                json={"first_name": first_name, "last_name": last_name},
                timeout=15,
            )
            if response.status_code == 200:
                return True, response.json()
            return False, response.json().get("detail", "No se pudo actualizar")
        except Exception as e:
            return False, str(e)

    # --- elections
    def list_elections(self) -> tuple[bool, List[Dict[str, Any]] | str]:
        try:
            resp = requests.get(f"{self.base_url}/election/elections", timeout=15)
            if resp.status_code == 200:
                return True, resp.json()
            return False, resp.text
        except Exception as e:
            return False, str(e)

    def election_candidates(self, election_id: str) -> tuple[bool, List[Dict[str, Any]] | str]:
        try:
            resp = requests.get(f"{self.base_url}/election/{election_id}/candidates", timeout=15)
            if resp.status_code == 200:
                return True, resp.json()
            return False, resp.text
        except Exception as e:
            return False, str(e)

    # --- votes
    def list_votes(self) -> tuple[bool, List[Dict[str, Any]] | str]:
        try:
            resp = requests.get(f"{self.base_url}/vote/", timeout=15)
            if resp.status_code == 200:
                return True, resp.json()
            return False, resp.text
        except Exception as e:
            return False, str(e)

    def vote(self, token: str, candidate_id: str, election_id: str) -> tuple[bool, Any]:
        try:
            resp = requests.post(
                f"{self.base_url}/vote/create-vote",
                headers=self._auth_headers(token),
                params={"candidate_id": candidate_id, "election_id": election_id},
                timeout=15,
            )
            if resp.status_code == 200:
                return True, resp.json()
            return False, resp.json().get("detail", "No se pudo registrar el voto")
        except Exception as e:
            return False, str(e)



