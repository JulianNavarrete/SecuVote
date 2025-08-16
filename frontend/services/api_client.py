import os
from typing import Dict, Optional, Any, List
import requests


class ApiClient:
	def __init__(self, base_url: Optional[str] = None):
		self.base_url = base_url or os.environ.get("SECUVOTE_API", "http://localhost:8000/api/v1")
		self.session = requests.Session()
		self.access_token: Optional[str] = None

	def set_token(self, token: Optional[str]):
		self.access_token = token

	def _headers(self) -> Dict[str, str]:
		headers = {"Content-Type": "application/json"}
		if self.access_token:
			headers["Authorization"] = f"Bearer {self.access_token}"
		return headers

	# Auth
	def login(self, dni: str, password: str) -> Dict[str, Any]:
		url = f"{self.base_url}/auth/login"
		# FastAPI expects OAuth2PasswordRequestForm fields
		data = {"username": dni, "password": password}
		response = self.session.post(url, data=data)
		response.raise_for_status()
		return response.json()

	def me(self) -> Dict[str, Any]:
		url = f"{self.base_url}/user/me"
		response = self.session.get(url, headers=self._headers())
		response.raise_for_status()
		return response.json()

	def update_me(self, data: Dict[str, Any]) -> Dict[str, Any]:
		url = f"{self.base_url}/user/update"
		response = self.session.post(url, json=data, headers=self._headers())
		response.raise_for_status()
		return response.json()

	def signup(self, email: str, dni: int, password: str) -> Dict[str, Any]:
		url = f"{self.base_url}/user/create"
		payload = {"email": email, "dni": dni, "password": password}
		response = self.session.post(url, json=payload)
		response.raise_for_status()
		return response.json()

	# Elections
	def list_elections(self) -> List[Dict[str, Any]]:
		url = f"{self.base_url}/election/elections"
		response = self.session.get(url)
		response.raise_for_status()
		return response.json()

	def election_candidates(self, election_id: str) -> List[Dict[str, Any]]:
		url = f"{self.base_url}/election/{election_id}/candidates"
		response = self.session.get(url)
		response.raise_for_status()
		return response.json()

	# Votes
	def create_vote(self, candidate_id: str, election_id: str) -> Dict[str, Any]:
		url = f"{self.base_url}/vote/create-vote"
		params = {"candidate_id": candidate_id, "election_id": election_id}
		response = self.session.post(url, params=params, headers=self._headers())
		response.raise_for_status()
		return response.json()

	def list_votes(self) -> List[Dict[str, Any]]:
		url = f"{self.base_url}/vote/"
		response = self.session.get(url)
		response.raise_for_status()
		return response.json()

	def has_voted(self, election_id: str) -> bool:
		url = f"{self.base_url}/vote/has-voted"
		params = {"election_id": election_id}
		response = self.session.get(url, params=params, headers=self._headers())
		response.raise_for_status()
		return bool(response.json().get("has_voted"))


