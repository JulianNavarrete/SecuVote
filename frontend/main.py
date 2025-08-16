import os
import streamlit as st

# Basic configuration
st.set_page_config(page_title="SecuVote", page_icon="🗳️", layout="centered")

# Simple router
pages = {
	"views/login_view.py": "Login",
	"views/signup_view.py": "Registro",
	"views/home_view.py": "Inicio",
	"views/election_view.py": "Elección",
	"views/vote_view.py": "Votar",
	"views/profile_view.py": "Perfil",
}

# Load initial view
if "_page" not in st.session_state:
	st.session_state["_page"] = "views/login_view.py"


def switch_page(page_path: str):
	st.session_state["_page"] = page_path
	st.rerun()


st.switch_page = switch_page  # type: ignore


def _render_current_page():
	current = st.session_state.get("_page", "views/login_view.py")
	# Dynamic import
	module_name = current.replace("/", ".").replace(".py", "")
	module = __import__(module_name, fromlist=["render"])
	module.render()


_render_current_page()


