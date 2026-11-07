# SkillSetu

SkillSetu is organized as a backend API and frontend application.

## Backend quick start

From the repository root:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The API is available at `http://127.0.0.1:8000`, with interactive
documentation at `http://127.0.0.1:8000/docs` and a health check at
`http://127.0.0.1:8000/health`.
