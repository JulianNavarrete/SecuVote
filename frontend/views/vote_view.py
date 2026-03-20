import streamlit as st
import requests
from app_state import get_client, get_auth
from datetime import datetime, timezone


def _election_open_status(election):
	start = election.get("start_date")
	end = election.get("end_date")
	if start is None and end is None:
		return True, None
	now = datetime.now(timezone.utc)
	if isinstance(start, str):
		start = datetime.fromisoformat(start.replace("Z", "+00:00"))
	if isinstance(end, str):
		end = datetime.fromisoformat(end.replace("Z", "+00:00"))
	if start is not None and getattr(start, "tzinfo", None) is None:
		start = start.replace(tzinfo=timezone.utc)
	if end is not None and getattr(end, "tzinfo", None) is None:
		end = end.replace(tzinfo=timezone.utc)
	if start is not None and now < start:
		return False, "not_open"
	if end is not None and now > end:
		return False, "closed"
	return True, None


def _candidate_vote_label(candidate):
	"""Texto mostrado al votar: nombre - biografía."""
	name = (candidate.get("name") or "").strip()
	bio = (candidate.get("bio") or "").strip()
	if bio:
		return f"{name} - {bio}"
	return name


def render():
	auth = get_auth()
	if not auth.access_token:
		st.info("Debes iniciar sesión")
		st.switch_page("views/login_view.py")
		return

	election = st.session_state.get("current_election")
	candidates = st.session_state.get("vote_candidates", [])
	if not election:
		st.warning("No hay elección seleccionada")
		st.switch_page("views/home_view.py")
		return

	is_open, reason = _election_open_status(election)
	if not is_open:
		if reason == "not_open":
			st.warning("Esta elección aún no está abierta para votar.")
		else:
			st.warning("Esta elección ya cerró; no se pueden registrar más votos.")
		if st.button("Volver a la elección"):
			st.switch_page("views/election_view.py")
		return

	st.title(f"Votar en {election['name']}")
	options = {}
	seen = {}
	for c in candidates:
		label = _candidate_vote_label(c)
		n = seen.get(label, 0)
		seen[label] = n + 1
		if n:
			label = f"{label} ({n + 1})"
		options[label] = c["id"]
	choice = st.radio("Selecciona tu candidato", list(options.keys()))

	if st.button("Confirmar voto"):
		try:
			client = get_client()
			vote = client.create_vote(candidate_id=options[choice], election_id=election["id"])
			st.success("¡Voto registrado!")
			st.balloons()
			st.switch_page("views/home_view.py")
		except requests.HTTPError as e:
			if e.response.status_code == 400:
				try:
					detail = (e.response.json() or {}).get("detail", "")
					if "already voted" in detail.lower():
						st.warning("Ya registraste un voto en esta elección.")
						st.switch_page("views/election_view.py")
					elif "not opened" in detail.lower() or "already closed" in detail.lower():
						st.warning("La elección no está abierta para votar en este momento.")
						st.switch_page("views/election_view.py")
					else:
						st.error(f"No se pudo registrar el voto: {detail or e}")
				except Exception:
					st.error(f"No se pudo registrar el voto: {e}")
			else:
				st.error(f"No se pudo registrar el voto: {e}")
		except Exception as e:
			st.error(f"No se pudo registrar el voto: {e}")

	if st.button("Cancelar"):
		st.switch_page("views/election_view.py")



