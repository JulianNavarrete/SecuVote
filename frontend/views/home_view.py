import streamlit as st
import re
from app_state import get_client, get_auth


def _elections_sorted_for_home(elections: list[dict]) -> list[dict]:
	"""
	Orden mostrado en home:
	- Primero por año detectado (ascendente para que 2023 aparezca antes que 2027).
	- Luego por ronda (1ra/segunda) para que 2023 1ra vaya antes que 2023 segunda.
	- Dentro del mismo "año+ronda", orden alfabético descendente: por `name` y desempate por `description` ("bio").
	- Si no se puede detectar el patrón, fallback al orden alfabético descendente.
	"""

	def _year_round(e: dict) -> tuple[int, int]:
		name = str(e.get("name") or "")
		desc = str(e.get("description") or "")
		text = f"{name} {desc}"

		year_match = re.search(r"(19\d{2}|20\d{2})", text)
		year = int(year_match.group(1)) if year_match else 10**9

		t = text.lower()
		if re.search(r"\b(1ra|primera)\b", t):
			round_order = 1
		elif re.search(r"\b(2da|segunda)\b", t):
			round_order = 2
		elif re.search(r"\b(3ra|tercera)\b", t):
			round_order = 3
		else:
			round_order = 99

		return year, round_order

	def _alphabetical_desc_key(e: dict) -> tuple[str, str]:
		# `description` es lo que la UI muestra como caption, por eso lo usamos como "bio".
		name = str(e.get("name") or "").lower()
		desc = str(e.get("description") or "").lower()
		return name, desc

	# Paso 1: orden alfabético descendente (estable).
	elections = sorted(elections, key=_alphabetical_desc_key, reverse=True)
	# Paso 2: reordenamos por (año, ronda) ascendente. Al ser estable,
	# se mantiene el orden alfabético descendente dentro de cada grupo.
	elections = sorted(elections, key=_year_round)
	return elections


def render():
	auth = get_auth()
	st.title("Inicio")

	if not auth.access_token:
		st.info("Debes iniciar sesión")
		if st.button("Ir al login"):
			st.switch_page("views/login_view.py")
		return

	user = auth.user
	with st.sidebar:
		st.subheader("Usuario")
		if user:
			st.write(f"{user.get('email')} (DNI {user.get('dni')})")
			if st.button("Modificar usuario"):
				st.switch_page("views/profile_view.py")
		if st.button("Cerrar sesión"):
			auth.access_token = None
			auth.refresh_token = None
			auth.user = None
			st.switch_page("views/login_view.py")

	st.subheader("Elecciones disponibles")
	try:
		client = get_client()
		elections = client.list_elections()
		elections = _elections_sorted_for_home(elections)
		for e in elections:
			with st.container(border=True):
				st.write(f"{e['name']}")
				st.caption(e.get("description", ""))
				if st.button("Ver", key=f"view_{e['id']}"):
					st.session_state["current_election"] = e
					st.switch_page("views/election_view.py")
	except Exception as ex:
		st.error(f"Error al cargar elecciones: {ex}")


