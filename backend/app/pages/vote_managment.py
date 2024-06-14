import streamlit as st
import requests

# Título de la página
st.title("Gestión de Votos")

# URL base de la API
BASE_URL = "http://localhost:8000"

# Función para crear un voto
def create_vote(dni, candidate_id, election_id):
    data = {
        "dni": dni,
        "candidate_id": candidate_id,
        "election_id": election_id
    }
    response = requests.post(f"{BASE_URL}/create-vote", json=data)
    if response.status_code == 200:
        return response.json()
    else:
        return {"detail": response.text}

# Función para obtener un voto por ID
def get_vote_by_id(vote_id):
    response = requests.get(f"{BASE_URL}/vote/{vote_id}")
    if response.status_code == 200:
        return response.json()
    else:
        return {"detail": response.text}

# Función para obtener todos los votos
def get_all_votes():
    response = requests.get(f"{BASE_URL}/")
    if response.status_code == 200:
        return response.json()
    else:
        return {"detail": response.text}

# Sección para crear un nuevo voto
st.header("Crear Nuevo Voto")
dni = st.number_input("DNI")
candidate_id = st.text_input("ID del Candidato")
election_id = st.text_input("ID de la Elección")
if st.button("Crear Voto"):
    response = create_vote(dni, candidate_id, election_id)
    st.write(response)

# Sección para obtener un voto por ID
st.header("Obtener Voto por ID")
vote_id = st.text_input("ID del Voto")
if st.button("Obtener Voto"):
    vote = get_vote_by_id(vote_id)
    st.write(vote)
    

# Sección para obtener todos los votos
st.header("Obtener Todos los Votos")
if st.button("Obtener Todos los Votos"):
    votes = get_all_votes()
    st.write(votes)
