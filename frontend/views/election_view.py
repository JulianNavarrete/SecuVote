import streamlit as st
from app_state import get_client


def render():
	election = st.session_state.get("current_election")
	if not election:
		st.warning("No hay elección seleccionada")
		st.switch_page("views/home_view.py")
		return

	st.title(election["name"])
	st.caption(election.get("description", ""))

	st.subheader("Candidatos")
	client = get_client()
	try:
		candidates = client.election_candidates(election["id"])
		# local vote count for each candidate (if votes are available)
		vote_counts = {}
		try:
			votes = client.list_votes()
			for v in votes:
				if v.get("election") == election["id"]:
					cid = v.get("candidate")
					vote_counts[cid] = vote_counts.get(cid, 0) + 1
		except Exception:
			vote_counts = {}

		# check if logged user has already voted on this election
		try:
			already_voted = client.has_voted(election_id=election["id"])
		except Exception:
			already_voted = False
	except Exception as e:
		st.error(f"No se pudieron cargar los candidatos: {e}")
		return

	for c in candidates:
		with st.container(border=True):
			count = vote_counts.get(c["id"], 0)
			st.write(f"{c['name']} - {c.get('party','')}")
			st.caption(f"Votos: {count}")
			if c.get("bio"):
				st.caption(c["bio"])

	# button to go to vote (only if not already voted)
	if (not already_voted) and st.button("Votar"):
		st.session_state["vote_candidates"] = candidates
		st.switch_page("views/vote_view.py")

	if already_voted:
		st.info("Ya emitiste tu voto en esta elección.")

	if st.button("Volver"):
		st.switch_page("views/home_view.py")


