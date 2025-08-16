import streamlit as st
from app_state import get_client, get_auth


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
		for e in elections:
			with st.container(border=True):
				st.write(f"{e['name']}")
				st.caption(e.get("description", ""))
				col1, col2 = st.columns([1,1])
				with col1:
					if st.button("Ver", key=f"view_{e['id']}"):
						st.session_state["current_election"] = e
						st.switch_page("views/election_view.py")
				with col2:
					st.write("")
	except Exception as ex:
		st.error(f"Error al cargar elecciones: {ex}")


