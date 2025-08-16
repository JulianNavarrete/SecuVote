.venv\Scripts\Activate.ps1
if (-not $env:SECUVOTE_API) { $env:SECUVOTE_API="http://localhost:8001/api/v1" }
streamlit run main.py --server.headless true
