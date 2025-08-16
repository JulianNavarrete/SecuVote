import streamlit as st
from app_state import get_client, get_auth


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

	st.title(f"Votar en {election['name']}")
	options = {c["name"]: c["id"] for c in candidates}
	choice = st.radio("Selecciona tu candidato", list(options.keys()))

	if st.button("Confirmar voto"):
		try:
			client = get_client()
			vote = client.create_vote(candidate_id=options[choice], election_id=election["id"])
			st.success("¡Voto registrado!")
			st.balloons()
			st.switch_page("views/home_view.py")
		except Exception as e:
			# handle case already voted
			msg = str(e)
			if "already voted" in msg.lower() or "400 Client Error" in msg:
				st.warning("Ya registraste un voto en esta elección.")
				st.switch_page("views/election_view.py")
			else:
				st.error(f"No se pudo registrar el voto: {e}")

	if st.button("Cancelar"):
		st.switch_page("views/election_view.py")


