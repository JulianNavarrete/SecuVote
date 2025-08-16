import streamlit as st
from app_state import get_client, get_auth, set_tokens


def render():
	st.title("Iniciar sesión")

	with st.form("login_form", clear_on_submit=False):
		dni = st.text_input("DNI", value="")
		password = st.text_input("Contraseña", type="password")
		col1, col2 = st.columns([1,1])
		with col1:
			submitted = st.form_submit_button("Ingresar")
		with col2:
			st.link_button("¿Olvidaste tu contraseña?", "#", help="Placeholder, aún no implementado")

	if submitted:
		try:
			client = get_client()
			tokens = client.login(dni=dni, password=password)
			set_tokens(tokens.get("access_token"), tokens.get("refresh_token"))
			# save active user
			user = client.me()
			get_auth().user = user
			st.session_state["user"] = user
			st.success("Sesión iniciada")
			st.switch_page("views/home_view.py")
		except Exception as e:
			st.error(f"No se pudo iniciar sesión: {e}")

	st.caption("¿No tienes cuenta?")
	if st.button("Crear cuenta"):
		st.switch_page("views/signup_view.py")


