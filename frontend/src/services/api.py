import httpx
from typing import Optional


BASE_URL = "http://localhost:8001/api/v1"


async def login(dni: int, password: str) -> Optional[dict]:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{BASE_URL}/auth/login",
                data={
                    "username": str(dni),  # Backend expects DNI as username
                    "password": password
                }
            )
            if response.status_code == 200:
                return response.json()
            return None
    except Exception as e:
        print(f"Error en login: {e}")
        return None


async def register(email: str, dni: int, password: str) -> Optional[dict]:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{BASE_URL}/user/create",
                json={
                    "email": email,
                    "dni": dni,
                    "password": password
                }
            )
            if response.status_code == 200:
                return response.json()
            return None
    except Exception as e:
        print(f"Error en registro: {e}")
        return None


async def get_elections() -> Optional[list]:
    try:
        async with httpx.AsyncClient() as client:
            token = page.session.get("access_token")
            response = await client.get(
                f"{BASE_URL}/election/",
                headers={"Authorization": f"Bearer {token}"}
            )
            if response.status_code == 200:
                return response.json()
            return None
    except Exception as e:
        print(f"Error obteniendo elecciones: {e}")
        return None


async def get_candidates(election_id: str) -> Optional[list]:
    try:
        async with httpx.AsyncClient() as client:
            token = page.client_storage.get("access_token")
            response = await client.get(
                f"{BASE_URL}/election/{election_id}/candidates",
                headers={"Authorization": f"Bearer {token}"}
            )
            if response.status_code == 200:
                return response.json()
            return None
    except Exception as e:
        print(f"Error obteniendo candidatos: {e}")
        return None

