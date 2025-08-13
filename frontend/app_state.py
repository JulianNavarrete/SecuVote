from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class AppState:

    api_base_url: str = "http://localhost:8000/api/v1"
    access_token: Optional[str] = None
    current_user: Optional[Dict[str, Any]] = None
    current_election: Optional[Dict[str, Any]] = None

    def set_token(self, token: Optional[str]) -> None:
        self.access_token = token

    def set_user(self, user: Optional[Dict[str, Any]]) -> None:
        self.current_user = user

    def set_election(self, election: Optional[Dict[str, Any]]) -> None:
        self.current_election = election



