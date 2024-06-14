import streamlit as st

st.title("SecuVote")

st.sidebar.title("Navigation")
pages = ["Home", "User managment", ""]

page = st.sidebar.radio("Go to", pages)

if page == "Home":
    st.write("Welcome to the future of the election voting system!")
elif page == "User managment":
    st.write("User managment.")
    from pages import user_management
    user_management.run()
elif page == "Create Candidate":
    st.write("Create a new candidate.")
    from pages import create_candidate
    create_candidate.run()
elif page == "Vote Candidate":
    st.write("Vote for a candidate.")
    from pages import vote_candidate
    vote_candidate.run()
elif page == "Create Election":
    st.write("Create a new election.")
    from pages import create_election
    create_election.run()
elif page == "Create User":
    st.write("Create a new user.")
    from pages import create_user
    create_user.run()
elif page == "Get Candidates":
    st.write("List of all candidates.")
    from pages import get_candidates
    get_candidates.run()
elif page == "Get Elections":
    st.write("List of all elections.")
    from pages import get_elections
    get_elections.run()
