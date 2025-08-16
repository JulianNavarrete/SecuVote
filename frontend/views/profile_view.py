import streamlit as st
from app_state import get_auth, get_client


def render():
	auth = get_auth()
	st.title("Perfil")
	if not auth.user:
		st.info("Inicia sesión para ver tu perfil")
		return

	client = get_client()
	user = auth.user

	with st.form("user_edit_form"):
		email = st.text_input("Email", value=user.get("email", ""))
		first_name = st.text_input("Nombre", value=user.get("first_name", "") or "")
		last_name = st.text_input("Apellido", value=user.get("last_name", "") or "")
		submitted = st.form_submit_button("Guardar cambios")

	if submitted:
		try:
			payload = {"email": email, "first_name": first_name, "last_name": last_name}
			updated = client.update_me(payload)
			auth.user = updated
			st.success("Datos actualizados")
		except Exception as e:
			st.error(f"No se pudo actualizar: {e}")

	if st.button("Volver"):
		st.switch_page("views/home_view.py")


