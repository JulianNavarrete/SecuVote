import streamlit as st
from app_state import get_client
from datetime import datetime, timezone


def _election_open_status(election):
	# check if the election is open or closed. if start_date is None and end_date is None, the election is open.
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


def render():
	election = st.session_state.get("current_election")
	if not election:
		st.warning("No hay elección seleccionada")
		st.switch_page("views/home_view.py")
		return

	is_open, reason = _election_open_status(election)

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

	# button to vote only if the election is open and the user has not voted
	if not is_open:
		if reason == "not_open":
			st.warning("Esta elección aún no está abierta para votar.")
		else:
			st.warning("Esta elección ya cerró; no se pueden registrar más votos.")
	elif not already_voted and st.button("Votar"):
		st.session_state["vote_candidates"] = candidates
		st.switch_page("views/vote_view.py")

	if already_voted:
		st.info("Ya emitiste tu voto en esta elección.")

	if st.button("Volver"):
		st.switch_page("views/home_view.py")


