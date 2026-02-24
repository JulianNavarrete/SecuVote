import os
import streamlit as st

# Basic configuration
st.set_page_config(
	page_title="SecuVote",
	page_icon="🗳️",
	layout="centered",
	initial_sidebar_state="auto",
)

# Estilos globales: barra lateral, contenedores y aspecto general
st.markdown(
	"""
	<style>
	/* Botón para abrir/cerrar la barra lateral: aspecto de menú, más visible */
	[data-testid="stSidebar"] > div:first-child button,
	[data-testid="collapsedControl"] button {
		background: linear-gradient(135deg, #1a5f7a 0%, #159895 100%) !important;
		color: white !important;
		border-radius: 10px !important;
		padding: 0.45rem 0.6rem !important;
	}
	[data-testid="stSidebar"] > div:first-child button:hover,
	[data-testid="collapsedControl"] button:hover {
		box-shadow: 0 4px 12px rgba(26, 95, 122, 0.35) !important;
	}
	/* Barra lateral: fondo y borde */
	[data-testid="stSidebar"] {
		background: linear-gradient(180deg, #ffffff 0%, #f1f5f9 100%) !important;
		border-right: 1px solid #e2e8f0 !important;
	}
	[data-testid="stSidebar"] .stMarkdown {
		color: #1e293b !important;
	}
	/* Contenedores con borde (cards de elecciones, candidatos, etc.) */
	[data-testid="stVerticalBlockBorderWrapper"] {
		border-radius: 12px !important;
		box-shadow: 0 1px 3px rgba(0,0,0,0.06) !important;
		border: 1px solid #e2e8f0 !important;
		padding: 1rem 1.25rem !important;
	}
	/* Botones más redondeados y coherentes */
	.stButton > button {
		border-radius: 10px !important;
		font-weight: 500 !important;
		transition: box-shadow 0.2s ease !important;
	}
	.stButton > button:hover {
		box-shadow: 0 4px 12px rgba(26, 95, 122, 0.2) !important;
	}
	/* Inputs con bordes redondeados */
	.stTextInput > div > div > input,
	.stNumberInput > div > div > input {
		border-radius: 10px !important;
	}
	/* Títulos con un poco más de aire */
	h1, .stMarkdown h1 {
		color: #1a5f7a !important;
		font-weight: 700 !important;
		margin-bottom: 0.5rem !important;
	}
	h2, .stMarkdown h2, .stSubheader {
		color: #334155 !important;
		font-weight: 600 !important;
	}
	/* Área principal con padding consistente */
	.block-container {
		padding-top: 2rem !important;
		padding-bottom: 2rem !important;
		max-width: 720px !important;
	}
	/* Formularios: separación entre campos */
	[data-testid="stForm"] {
		border-radius: 12px !important;
	}
	</style>
	""",
	unsafe_allow_html=True,
)

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


