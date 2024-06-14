import streamlit as st
import requests
from typing import Optional

# Base URL of the FastAPI backend
BASE_URL = "http://localhost:8000/api/v1"

def create_candidate():
    st.title("Create Candidate")
    name = st.text_input("Name")
    party = st.text_input("Party")
    bio = st.text_area("Bio")
    if st.button("Create Candidate"):
        candidate_data = {"name": name, "party": party, "bio": bio}
        response = requests.post(f"{BASE_URL}/candidate/create-candidate", json=candidate_data)
        if response.status_code == 200:
            st.success("Candidate created successfully!")
        else:
            st.error("Failed to create candidate. " + response.json().get("detail", "Unknown error"))

def get_candidate_details():
    st.title("Get Candidate Details")
    candidate_id = st.text_input("Candidate ID")
    if st.button("Get Candidate Details"):
        response = requests.get(f"{BASE_URL}/candidate/candidate/{candidate_id}")
        if response.status_code == 200:
            candidate_details = response.json()
            st.json(candidate_details)
        else:
            st.error("Failed to retrieve candidate details. " + response.json().get("detail", "Unknown error"))

def update_candidate():
    st.title("Update Candidate")
    candidate_id = st.text_input("Candidate ID")
    name = st.text_input("Name")
    party = st.text_input("Party")
    bio = st.text_area("Bio")
    if st.button("Update Candidate"):
        candidate_data = {"name": name, "party": party, "bio": bio}
        response = requests.post(f"{BASE_URL}/candidate/update-candidate/{candidate_id}", json=candidate_data)
        if response.status_code == 200:
            st.success("Candidate updated successfully!")
        else:
            st.error("Failed to update candidate. " + response.json().get("detail", "Unknown error"))

def delete_candidate():
    st.title("Delete Candidate")
    candidate_id = st.text_input("Candidate ID")
    if st.button("Delete Candidate"):
        response = requests.delete(f"{BASE_URL}/candidate/delete-candidate/{candidate_id}")
        if response.status_code == 200:
            st.success("Candidate deleted successfully!")
        else:
            st.error("Failed to delete candidate. " + response.json().get("detail", "Unknown error"))

def add_election_to_candidate():
    st.title("Add Election to Candidate")
    candidate_id = st.text_input("Candidate ID")
    election_id = st.text_input("Election ID")
    if st.button("Add Election"):
        response = requests.post(f"{BASE_URL}/candidate/add-election-to-candidate/{candidate_id}/{election_id}")
        if response.status_code == 200:
            st.success("Election added to candidate successfully!")
        else:
            st.error("Failed to add election to candidate. " + response.json().get("detail", "Unknown error"))

def remove_election_from_candidate():
    st.title("Remove Election from Candidate")
    candidate_id = st.text_input("Candidate ID")
    election_id = st.text_input("Election ID")
    if st.button("Remove Election"):
        response = requests.delete(f"{BASE_URL}/candidate/remove-election-from-candidate/{candidate_id}/{election_id}")
        if response.status_code == 200:
            st.success("Election removed from candidate successfully!")
        else:
            st.error("Failed to remove election from candidate. " + response.json().get("detail", "Unknown error"))

def main():
    st.sidebar.title("Candidate Management")
    option = st.sidebar.selectbox("Choose an option", [
        "Create Candidate", 
        "Get Candidate Details", 
        "Update Candidate", 
        "Delete Candidate", 
        "Add Election to Candidate", 
        "Remove Election from Candidate"
    ])

    if option == "Create Candidate":
        create_candidate()
    elif option == "Get Candidate Details":
        get_candidate_details()
    elif option == "Update Candidate":
        update_candidate()
    elif option == "Delete Candidate":
        delete_candidate()
    elif option == "Add Election to Candidate":
        add_election_to_candidate()
    elif option == "Remove Election from Candidate":
        remove_election_from_candidate()

if __name__ == "__main__":
    main()
