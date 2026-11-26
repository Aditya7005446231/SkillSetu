# SkillSetu (CareerBridge AI)

SkillSetu is an AI-powered student career workflow and opportunity matching platform that analyzes student resumes, normalizes skills via an in-memory RAG skill framework, scores fit against active internship/job openings, and builds personalized skill-gap learning roadmaps.

---

## Architecture Overview

- **Backend:** FastAPI (Python 3.11), PyMuPDF (PDF text extraction), Groq Cloud API (structured profiling and reasoning), In-Memory Vector RAG (`all-MiniLM-L6-v2` ONNX + NumPy matrix dot-product).
- **Database:** Supabase PostgreSQL with PostgREST and Row Level Security (RLS).
- **Frontend:** React 19 + Vite SPA, Lucide React icons, Tailwind CSS / Vanilla CSS tokens.
- **Job Ingestion:** JSearch (OpenWebNinja) API sync.

---

## Prerequisites

- **Python:** 3.11 or higher
- **Node.js:** v18 or higher (with npm)
- **Supabase Account:** for authentication and PostgreSQL database
- **Groq API Key:** for LLM extraction and agent planning

---

## 1. Database Setup (Supabase)

1. Create a new project on [Supabase](https://supabase.com).
2. Go to the **SQL Editor** in your Supabase dashboard.
3. Sequentially open and run the numbered migration scripts located in `backend/sql/`:
   - `000_base_schema.sql` (Creates core tables: `profiles`, `skills`, `student_skills`, `projects`, `jobs`, `job_skills`)
   - `001_opportunity_tracking.sql`
   - `002_opportunity_rls.sql`
   - `003_candidate_state.sql`
   - `004_multi_resume.sql`
   - `005_learning_progress.sql`

Refer to [backend/sql/README.md](backend/sql/README.md) for full migration details.

---

## 2. Backend Setup & Run

1. Open a terminal and navigate to the `backend/` directory:
   ```bash
   cd backend
   ```

2. Create and activate a Python virtual environment:
   ```bash
   # On Windows (PowerShell):
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1

   # On macOS/Linux:
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   ```bash
   cp .env.example .env
   ```
   Fill in your actual keys in `backend/.env`:
   - `SUPABASE_URL`: Your Supabase Project URL (`https://<project-ref>.supabase.co`)
   - `SUPABASE_ANON_KEY` or `SUPABASE_SECRET_KEY`: Supabase publishable anon key
   - `SUPABASE_SERVICE_ROLE_KEY`: Supabase service role secret key
   - `GROQ_API_KEY`: Your Groq Cloud API Key
   - `OPENWEBNINJA_API_KEY`: (Optional) For live job sync from JSearch

5. Start the FastAPI backend server:
   ```bash
   python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
   ```
   The API will be live at `http://127.0.0.1:8000`.
   - Health check: `http://127.0.0.1:8000/health`
   - Interactive Swagger API docs: `http://127.0.0.1:8000/docs`

---

## 3. Frontend Setup & Run

1. In a separate terminal, navigate to the `frontend/` directory:
   ```bash
   cd frontend
   ```

2. Configure frontend environment variables:
   ```bash
   cp .env.example .env
   ```
   Set the Supabase credentials matching your backend:
   ```env
   VITE_API_URL=http://localhost:8000
   VITE_SUPABASE_URL=https://<your-project>.supabase.co
   VITE_SUPABASE_ANON_KEY=<your-supabase-anon-key>
   ```

3. Install frontend dependencies:
   ```bash
   npm install
   ```

4. Run the Vite development server:
   ```bash
   npm run dev
   ```
   Open your browser and navigate to `http://localhost:5173`.

---

## 4. Verification & Testing

### Backend Unit & Integration Tests
From the project root:
```bash
python -m unittest discover -s backend -p "test_*.py"
```

### In-Memory Vector RAG Suite
```bash
python -X utf8 backend/test_rag.py
```

### Frontend Production Build
```bash
cd frontend && npm run build
```
