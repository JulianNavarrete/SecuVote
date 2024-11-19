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
    
