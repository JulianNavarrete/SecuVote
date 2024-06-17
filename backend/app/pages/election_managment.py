import streamlit as st
import requests
from typing import Optional


# Base URL of the FastAPI backend
BASE_URL = "http://localhost:8000/api/v1"

def create_election():
    st.title("Create Election")
    name = st.text_input("Name")
    description = st.text_input("Description")
    start_date = st.date_input("Start Date")
    end_date = st.date_input("End Date")
    if st.button("Create Election"):
        election_data = {"name": name, "description": description, "start_date": start_date.strftime("%Y-%m-%d"), "end_date": end_date.strftime("%Y-%m-%d")}
        response = requests.post(f"{BASE_URL}/election/create-election", json=election_data.dict())
        if response.status_code == 200:
            st.success("Election created successfully!")
        else:
            st.error("Failed to create election. " + response.json().get("detail", "Unknown error"))

def get_election_details():
    st.title("Get Election Details")
    election_id = st.text_input("Election ID")
    if st.button("Get Election Details"):
        response = requests.get(f"{BASE_URL}/election/election/{election_id}")
        if response.status_code == 200:
            election_details = response.json()
            st.json(election_details)
        else:
            st.error("Failed to retrieve election details. " + response.json().get("detail", "Unknown error"))

def update_election():
    st.title("Update Election")
    election_id = st.text_input("Election ID")
    name = st.text_input("Name")
    party = st.text_input("Party")
    bio = st.text_area("Bio")
    if st.button("Update Election"):
        election_data = {"name": name, "party": party, "bio": bio}
        response = requests.post(f"{BASE_URL}/election/update-election/{election_id}", json=election_data)
        if response.status_code == 200:
            st.success("Election updated successfully!")
        else:
            st.error("Failed to update election. " + response.json().get("detail", "Unknown error"))

def delete_election():
    st.title("Delete Election")
    election_id = st.text_input("Election ID")
    if st.button("Delete Election"):
        response = requests.delete(f"{BASE_URL}/election/delete-election/{election_id}")
        if response.status_code == 200:
            st.success("Election deleted successfully!")
        else:
            st.error("Failed to delete election. " + response.json().get("detail", "Unknown error"))

def add_candidate_to_election():
    st.title("Add Candidate to Election")
    candidate_id = st.text_input("Candidate ID")
    election_id = st.text_input("Election ID")
    if st.button("Add Election"):
        response = requests.post(f"{BASE_URL}/election/add-candidate-to-election/{election_id}/{candidate_id}")
        if response.status_code == 200:
            st.success("Candidate added to election successfully!")
        else:
            st.error("Failed to add candidate to election. " + response.json().get("detail", "Unknown error"))

def remove_candidate_from_election():
    st.title("Remove candidate from election")
    candidate_id = st.text_input("Candidate ID")
    election_id = st.text_input("Election ID")
    if st.button("Remove Candidate"):
        response = requests.delete(f"{BASE_URL}/election/remove-candidate-from-election/{election_id}/{candidate_id}")
        if response.status_code == 200:
            st.success("Candidate removed from election successfully!")
        else:
            st.error("Failed to remove candidate from election. " + response.json().get("detail", "Unknown error"))

def main():
    st.sidebar.title("Election Management")
    option = st.sidebar.selectbox("Choose an option", [
        "Create Election", 
        "Get Election Details", 
        "Update Election", 
        "Delete Election", 
        "Add Candidate to Election", 
        "Remove Candidate from Election"
    ])

    if option == "Create Election":
        create_election()
    elif option == "Get Election Details":
        get_election_details()
    elif option == "Update Election":
        update_election()
    elif option == "Delete Election":
        delete_election()
    elif option == "Add Candidate to Election":
        add_candidate_to_election()
    elif option == "Remove Candidate from Election":
        remove_candidate_from_election()

if __name__ == "__main__":
    main()
