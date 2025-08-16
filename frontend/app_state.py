from dataclasses import dataclass, field
from typing import Optional, Dict, Any
import streamlit as st
from services.api_client import ApiClient


@dataclass
class AuthState:
	access_token: Optional[str] = None
	refresh_token: Optional[str] = None
	user: Optional[Dict[str, Any]] = None


def get_client() -> ApiClient:
	if "api_client" not in st.session_state:
		st.session_state["api_client"] = ApiClient()
	return st.session_state["api_client"]


def get_auth() -> AuthState:
	if "auth" not in st.session_state:
		st.session_state["auth"] = AuthState()
	return st.session_state["auth"]


def set_tokens(access: Optional[str], refresh: Optional[str]):
	auth = get_auth()
	auth.access_token = access
	auth.refresh_token = refresh
	client = get_client()
	client.set_token(access)


