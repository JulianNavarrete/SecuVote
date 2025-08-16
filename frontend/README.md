SecuVote Frontend (Streamlit)

Environment variables:
- `SECUVOTE_API`: Base URL for the FastAPI API, e.g: http://localhost:8001/api/v1

Quick installation (Windows):
1. Run `frontend/windows-install.ps1`
2. Run `frontend/windows-boot.ps1`

Structure:
- `main.py`: simple router between views
- `views/`: separate views (`login`, `signup`, `home`, `election`, `vote`, `profile`)
- `services/api_client.py`: HTTP client
- `app_state.py`: session state and tokens
