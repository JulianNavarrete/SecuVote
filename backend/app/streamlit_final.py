import streamlit as st
import requests

# Define the base URL for your FastAPI server
BASE_URL = "http://localhost:8000"

# Candidate Views
def create_candidate():
    st.title("Create a new Candidate")
    name = st.text_input("Name")
    party = st.text_input("Party")
    if st.button("Create"):
        response = requests.post(f"{BASE_URL}/create-candidate", json={"name": name, "party": party})
        if response.status_code == 200:
            st.success("Candidate created successfully")
        else:
            st.error(f"Error: {response.json().get('detail')}")

def get_candidate():
    st.title("Get Candidate Details")
    candidate_id = st.text_input("Candidate ID")
    if st.button("Get"):
        response = requests.get(f"{BASE_URL}/candidate/{candidate_id}")
        if response.status_code == 200:
            candidate = response.json()
            st.write(candidate)
        else:
            st.error(f"Error: {response.json().get('detail')}")

def update_candidate():
    st.title("Update Candidate")
    candidate_id = st.text_input("Candidate ID")
    name = st.text_input("New Name")
    party = st.text_input("New Party")
    if st.button("Update"):
        response = requests.post(f"{BASE_URL}/update-candidate/{candidate_id}", json={"name": name, "party": party})
        if response.status_code == 200:
            st.success("Candidate updated successfully")
        else:
            st.error(f"Error: {response.json().get('detail')}")

def delete_candidate():
    st.title("Delete Candidate")
    candidate_id = st.text_input("Candidate ID")
    if st.button("Delete"):
        response = requests.delete(f"{BASE_URL}/delete-candidate/{candidate_id}")
        if response.status_code == 200:
            st.success("Candidate deleted successfully")
        else:
            st.error(f"Error: {response.json().get('detail')}")

# Election Views
def create_election():
    st.title("Create a new Election")
    name = st.text_input("Name")
    if st.button("Create"):
        response = requests.post(f"{BASE_URL}/create", json={"name": name})
        if response.status_code == 200:
            st.success("Election created successfully")
        else:
            st.error(f"Error: {response.json().get('detail')}")

def get_election():
    st.title("Get Election Details")
    election_id = st.text_input("Election ID")
    if st.button("Get"):
        response = requests.get(f"{BASE_URL}/election/{election_id}")
        if response.status_code == 200:
            election = response.json()
            st.write(election)
        else:
            st.error(f"Error: {response.json().get('detail')}")

def update_election():
    st.title("Update Election")
    election_id = st.text_input("Election ID")
    name = st.text_input("New Name")
    if st.button("Update"):
        response = requests.post(f"{BASE_URL}/update-election/{election_id}", json={"name": name})
        if response.status_code == 200:
            st.success("Election updated successfully")
        else:
            st.error(f"Error: {response.json().get('detail')}")

def delete_election():
    st.title("Delete Election")
    election_id = st.text_input("Election ID")
    if st.button("Delete"):
        response = requests.delete(f"{BASE_URL}/delete-election/{election_id}")
        if response.status_code == 200:
            st.success("Election deleted successfully")
        else:
            st.error(f"Error: {response.json().get('detail')}")

# User Views
def create_user():
    st.title("Create a new User")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    dni = st.text_input("DNI")
    if st.button("Create"):
        response = requests.post(f"{BASE_URL}/create", json={"email": email, "password": password, "dni": dni})
        if response.status_code == 200:
            st.success("User created successfully")
        else:
            st.error(f"Error: {response.json().get('detail')}")

def get_me():
    st.title("Get My Details")
    if st.button("Get"):
        response = requests.get(f"{BASE_URL}/me")
        if response.status_code == 200:
            user = response.json()
            st.write(user)
        else:
            st.error(f"Error: {response.json().get('detail')}")

def update_user():
    st.title("Update User")
    email = st.text_input("New Email")
    password = st.text_input("New Password", type="password")
    dni = st.text_input("New DNI")
    if st.button("Update"):
        response = requests.post(f"{BASE_URL}/update", json={"email": email, "password": password, "dni": dni})
        if response.status_code == 200:
            st.success("User updated successfully")
        else:
            st.error(f"Error: {response.json().get('detail')}")

# Vote Views
def create_vote():
    st.title("Create a new Vote")
    dni = st.text_input("DNI")
    candidate_id = st.text_input("Candidate ID")
    election_id = st.text_input("Election ID")
    if st.button("Create"):
        response = requests.post(f"{BASE_URL}/create-vote", params={"dni": dni, "candidate_id": candidate_id, "election_id": election_id})
        if response.status_code == 200:
            st.success("Vote created successfully")
        else:
            st.error(f"Error: {response.json().get('detail')}")

def get_vote():
    st.title("Get Vote Details")
    vote_id = st.text_input("Vote ID")
    if st.button("Get"):
        response = requests.get(f"{BASE_URL}/vote/{vote_id}")
        if response.status_code == 200:
            vote = response.json()
            st.write(vote)
        else:
            st.error(f"Error: {response.json().get('detail')}")

def get_votes():
    st.title("Get All Votes")
    if st.button("Get All Votes"):
        response = requests.get(f"{BASE_URL}/vote/")
        if response.status_code == 200:
            votes = response.json()
            st.write(votes)
        else:
            st.error(f"Error: {response.json().get('detail')}")

# Main Function
def main():
    st.sidebar.title("Navigation")
    option = st.sidebar.selectbox("Select a View", [
        "Create Candidate", "Get Candidate", "Update Candidate", "Delete Candidate",
        "Create Election", "Get Election", "Update Election", "Delete Election",
        "Create User", "Get My Details", "Update User",
        "Create Vote", "Get Vote", "Get All Votes"
    ])
    
    if option == "Create Candidate":
        create_candidate()
    elif option == "Get Candidate":
        get_candidate()
    elif option == "Update Candidate":
        update_candidate()
    elif option == "Delete Candidate":
        delete_candidate()
    elif option == "Create Election":
        create_election()
    elif option == "Get Election":
        get_election()
    elif option == "Update Election":
        update_election()
    elif option == "Delete Election":
        delete_election()
    elif option == "Create User":
        create_user()
    elif option == "Get My Details":
        get_me()
    elif option == "Update User":
        update_user()
    elif option == "Create Vote":
        create_vote()
    elif option == "Get Vote":
        get_vote()
    elif option == "Get All Votes":
        get_votes()

if __name__ == "__main__":
    main()
