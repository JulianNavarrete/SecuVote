import streamlit as st
from app_state import get_client


def render():
	st.title("Crear cuenta")
	with st.form("signup_form", clear_on_submit=False):
		email = st.text_input("Email")
		dni = st.number_input("DNI", min_value=0, format="%d")
		password = st.text_input("Contraseña", type="password")
		submitted = st.form_submit_button("Registrarme")

	if submitted:
		try:
			client = get_client()
			client.signup(email=email, dni=int(dni), password=password)
			st.success("Usuario creado. Ahora inicia sesión.")
			st.switch_page("views/login_view.py")
		except Exception as e:
			st.error(f"No se pudo registrar: {e}")

	if st.button("Volver al login"):
		st.switch_page("views/login_view.py")


