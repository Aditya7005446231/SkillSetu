# SkillSetu architecture

## Backend

The backend is a FastAPI application under `backend/app`.

- `main.py` creates the FastAPI application and exposes system endpoints.
- `config.py` loads environment-backed application settings.
- `database.py` provides the SQLAlchemy engine, declarative base, and session dependency.
- `routes/` contains HTTP route modules.
- `agents/` contains agent implementations and orchestration.
- `services/` contains reusable application logic.
- `schemas/` contains Pydantic request and response models.

The default local database is SQLite. Set `DATABASE_URL` in `backend/.env` to use
another SQLAlchemy-compatible database.
