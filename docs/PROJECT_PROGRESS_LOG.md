# SkillSetu - Project Development & Change Log

This file tracks every architectural decision, completed task, database migration, code change, and testing procedure across the SkillSetu project.

---

## 📌 Executive Summary & Architecture

SkillSetu is an **Intelligent Career-Workflow Agent** that bridges the gap between students and the tech industry. It automates:
1. **Skill Profiling:** Parses resumes via PyMuPDF + Groq LLM, extracts verified skills, proficiencies, evidence, and projects.
2. **Opportunity Retrieval:** Ingests live job and internship listings (via JSearch/OpenWebNinja), extracting structured requirements and eligibility.
3. **In-Memory RAG over Skill Frameworks:** Uses a 232-document curated taxonomy with in-memory `all-MiniLM-L6-v2` ONNX dense vector embeddings via NumPy to canonicalize skills (`"ReactJS"` $\rightarrow$ `"React"`) and bridge skill gaps.
4. **Candidate State Persistence:** Stores student preferences and ranked match records in Supabase (`opportunity_matches` & `student_preferences`), enabling sub-50ms reload upon re-login.
5. **Conversational Refinement (Copilot):** Natural language chat allowing students to refine filters (e.g. *"remote internships in Bangalore with React"*), with LLM Pydantic validation and 1-retry error recovery.

---

## 🚦 Master Feature Status Checklist

| Feature | Category | Status | Implementation Details |
| :--- | :--- | :---: | :--- |
| **Resume Upload & Parsing** | Core Agent | 🟢 Done | `/api/resume/analyze`, PyMuPDF, `StudentProfile` Pydantic schema |
| **Live Job Ingestion** | Core Agent | 🟢 Done | `/api/opportunities/sync`, JSearch source adapter |
| **Deterministic Matching Engine** | Matching | 🟢 Done | `recommend_opportunities()`, skill coverage + location + type scoring |
| **Lightweight In-Memory RAG** | RAG | 🟢 Done | 232 docs, `all-MiniLM-L6-v2` ONNX + NumPy matrix dot-product |
| **Skill Canonicalization** | RAG | 🟢 Done | `normalize_skill()` (O(1) alias table + vector similarity threshold $\ge 0.58$) |
| **Skill Gap Bridging** | RAG | 🟢 Done | `get_related_skills()` returns complementary skills & prerequisites |
| **Candidate State Persistence** | Persistence | 🟢 Done | `opportunity_matches` table, auto-saved after each match run |
| **Student Preferences Store** | Persistence | 🟢 Done | `student_preferences` table with RLS and in-memory dev cache |
| **Fast Re-login Endpoint** | API | 🟢 Done | `GET /api/opportunities/saved` (<50ms retrieval) |
| **LLM Output Validation & Retry** | Safety | 🟢 Done | `call_llm_with_validation()` with 1 corrective retry loop |
| **Conversational Chatbot Endpoint** | Chat Agent | 🟢 Done | `POST /api/chat`, extracts `PreferenceUpdate`, re-runs matcher |
| **Interactive Frontend Copilot** | Frontend | 🟢 Done | `frontend/src/pages/Assistant.jsx` with chat history & live job cards |
| **Planner-Executor (`/api/agent/run`)** | Agent Orchestration | 🟢 Done | Groq `planner.py` + state machine `executor.py` (`profile`, `retrieve`, `match`, `roadmap`) |
| **Institutional Mock API** | API | 🟢 Done | `GET /api/institution/skills` campus placement-cell skill demand analytics |
| **Fairness Check Script** | Safety/Eval | 🟢 Done | `backend/test_fairness.py` counterfactual evaluation ($\Delta = 0.0$) $\rightarrow$ `docs/fairness_report.md` |
| **Monitoring & Metrics** | Ops | 🟡 Next Up | Request ID middleware + `GET /metrics` latency counter |
| **Production Deployment** | Ops | ⚪ Pending | Render backend + Vercel frontend configuration |

---

## 📝 Chronological Change Log

### Phase 1: In-Memory RAG Framework Upgrade
- **Problem:** Previous RAG prototype only had 11 documents with deterministic lexical keyword overlap and no embeddings.
- **Actions Taken:**
  1. Built [generate_framework.py](file:///d:/SkillSetu/backend/app/data/generate_framework.py) expanding the corpus to **232 documents** (8 industry roles and 224 granular skills) in [skill_framework.json](file:///d:/SkillSetu/backend/app/data/skill_framework.json).
  2. Downloaded and configured `all-MiniLM-L6-v2` ONNX model and tokenizer in `backend/app/data/models/all-MiniLM-L6-v2/` (bypassing Windows AppLocker DLL blocks with ONNX runtime).
  3. Precomputed normalized 384-dimensional dense vectors into [skill_embeddings.npy](file:///d:/SkillSetu/backend/app/data/skill_embeddings.npy) `(232, 384)`.
  4. Rewrote [skill_framework_rag.py](file:///d:/SkillSetu/backend/app/services/skill_framework_rag.py) with in-memory NumPy matrix dot-product search, hybrid lexical boosts, canonical normalization (`"ReactJS"` $\rightarrow$ `"React"`), and gap-bridging (`get_related_skills`).
  5. Built automated test script [backend/test_rag.py](file:///d:/SkillSetu/backend/test_rag.py) (All 6 test suites passed; 29.28 ms avg search latency).
  6. Updated documentation in [docs/rag-over-skill-frameworks.md](file:///d:/SkillSetu/docs/rag-over-skill-frameworks.md).

---

### Phase 2: Candidate State & SQL Migration
- **Problem:** Matches were computed on the fly and discarded. Re-login required re-computing 500 jobs from scratch, and user filters were lost.
- **Actions Taken:**
  1. Authored [backend/sql/candidate_state.sql](file:///d:/SkillSetu/backend/sql/candidate_state.sql) creating:
     - `public.student_preferences` (student search preferences, RLS protected).
     - `public.opportunity_matches` (candidate state table with `match_score`, `matched_skills`, `missing_skills`, `related_gap_skills`, `reason`).
     - Fixed foreign key incompatibility: `job_id` correctly typed as `bigint` to match `jobs.id`.
  2. Created [candidate_state_persistence.py](file:///d:/SkillSetu/backend/app/services/candidate_state_persistence.py) with functions:
     - `save_student_preferences()` & `get_student_preferences()`
     - `save_opportunity_matches()` & `get_saved_opportunity_matches()`
     - Built-in dev cache fallback so offline/local testing never crashes.
  3. Wired match auto-saving directly into `recommend_opportunities()` in [opportunity_matching.py](file:///d:/SkillSetu/backend/app/services/opportunity_matching.py).
  4. Added `GET /api/opportunities/saved` endpoint in [main.py](file:///d:/SkillSetu/backend/app/main.py) for instantaneous re-login loading.

---

### Phase 3: LLM Validation & Automated Retry Engine
- **Problem:** LLM responses can occasionally output malformed JSON or fail Pydantic schema validation.
- **Actions Taken:**
  1. Built [backend/app/services/llm_validator.py](file:///d:/SkillSetu/backend/app/services/llm_validator.py) with `call_llm_with_validation()`.
  2. Implemented automated 1-retry feedback loop: on `ValidationError` or `JSONDecodeError`, feeds the exact error trace back into Groq to self-correct.
  3. Integrated validation retry into:
     - [opportunity_agent.py](file:///d:/SkillSetu/backend/app/agents/opportunity_agent.py) (`ExtractedOpportunity`)
     - [skill_profiling.py](file:///d:/SkillSetu/backend/app/agents/skill_profiling.py) (`StudentProfile`)
     - [chat_agent.py](file:///d:/SkillSetu/backend/app/agents/chat_agent.py) (`PreferenceUpdate`)

---

### Phase 4: Conversational Refinement (Career Copilot)
- **Problem:** Students had no interactive chat interface to conversationally refine their recommendations.
- **Actions Taken:**
  1. Created schema [backend/app/schemas/preference.py](file:///d:/SkillSetu/backend/app/schemas/preference.py) (`PreferenceUpdate`, `ChatMessageRequest`, `ChatMessageResponse`).
  2. Built [backend/app/agents/chat_agent.py](file:///d:/SkillSetu/backend/app/agents/chat_agent.py) to parse conversational messages into structured filter deltas and canonicalize skills.
  3. Implemented `POST /api/chat` and `POST /api/chat-local` in [backend/app/main.py](file:///d:/SkillSetu/backend/app/main.py).
  4. Upgraded [frontend/src/pages/Assistant.jsx](file:///d:/SkillSetu/frontend/src/pages/Assistant.jsx) into a live interactive Copilot with chat history, quick prompt chips, filter badges, and inline refreshed job cards.
  5. Added **Career Copilot** (`Bot` icon) tab into main navigation in [frontend/src/App.jsx](file:///d:/SkillSetu/frontend/src/App.jsx).
  6. Verified complete end-to-end pipeline via [backend/test_conversational_refinement.py](file:///d:/SkillSetu/backend/test_conversational_refinement.py) (All 4 tests passed).

---

### Phase 5: Planner-Executor Agent Orchestration (`/api/agent/run`)
- **Problem:** Tasks were invoked as separate endpoints without autonomous planning or multi-step coordination.
- **Actions Taken:**
  1. Created [backend/app/schemas/agent_plan.py](file:///d:/SkillSetu/backend/app/schemas/agent_plan.py) defining `PlanStep`, `AgentPlan`, `AgentRunRequest`, and `AgentRunResponse`.
  2. Built [backend/app/agents/planner.py](file:///d:/SkillSetu/backend/app/agents/planner.py) using Groq LLM to decompose goals into an ordered capability plan chosen strictly from `["profile", "retrieve", "match", "roadmap"]`.
  3. Built [backend/app/agents/executor.py](file:///d:/SkillSetu/backend/app/agents/executor.py) with shared `AgentState` and `STEP_DISPATCH` mapping step names to execution functions (`step_profile`, `step_retrieve`, `step_match`, `step_roadmap`).
  4. Exposed `POST /api/agent/run` and `POST /api/agent/run-local` in [backend/app/main.py](file:///d:/SkillSetu/backend/app/main.py).
  5. Built and verified [backend/test_planner_executor.py](file:///d:/SkillSetu/backend/test_planner_executor.py) (All 4 tests passed, verifying planning, execution trace, match state, and roadmap milestones).

---

### Phase 6: Institutional Placement Cell API & Algorithmic Fairness Audit
- **Problem:** Need campus placement analytics for universities, and need proof that the matching algorithm does not discriminate based on protected demographic attributes (college tier, gender proxy, name).
- **Actions Taken:**
  1. Built [backend/app/schemas/institution.py](file:///d:/SkillSetu/backend/app/schemas/institution.py) defining `InstitutionalSkillDemand` and `InstitutionalDemandResponse`.
  2. Implemented `GET /api/institution/skills` in [backend/app/main.py](file:///d:/SkillSetu/backend/app/main.py) returning realistic mock campus hiring demand, YoY growth rates, role breakdowns, and curriculum gap recommendations.
  3. Created [backend/test_fairness.py](file:///d:/SkillSetu/backend/test_fairness.py) implementing a **Counterfactual Equivalence Audit**: evaluated three candidates with identical skills/projects (Rahul Sharma / IIT Bombay vs. Priya Patel / Tier-3 Rural College vs. Mohammed Zeeshan / Central Univ).
  4. Mathematically verified score delta $\Delta = 0.0$ across diverse job benchmarks.
  5. Auto-generated compliance audit report at [docs/fairness_report.md](file:///d:/SkillSetu/docs/fairness_report.md).

---

## 🗄️ Database Schema Reference

### `student_preferences`
| Column | Type | Description |
| :--- | :--- | :--- |
| `student_id` | `uuid` (PK) | References `profiles.id` (on delete cascade) |
| `preferred_location` | `text` | e.g. `"Bangalore"`, `"Remote"`, or empty |
| `remote_only` | `boolean` | `true` if candidate strictly wants remote roles |
| `preferred_job_type` | `text` | `"internship"`, `"full-time"`, etc. |
| `preferred_skills` | `jsonb` | Array of canonical skill strings |
| `target_role` | `text` | Target job title |
| `minimum_score` | `numeric` | Minimum match percentage threshold |
| `updated_at` | `timestamptz` | Last modification timestamp |

### `opportunity_matches`
| Column | Type | Description |
| :--- | :--- | :--- |
| `id` | `uuid` (PK) | Auto-generated UUID |
| `student_id` | `uuid` | References `profiles.id` (on delete cascade) |
| `job_id` | `bigint` | References `jobs.id` (on delete cascade) |
| `match_score` | `numeric` | Overall match percentage ($0 - 100$) |
| `matched_skills` | `jsonb` | Array of overlapping skills |
| `missing_skills` | `jsonb` | Array of required skills student lacks |
| `related_gap_skills`| `jsonb` | Map of missing skill $\rightarrow$ bridge skills |
| `reason` | `text` | Human-readable explanation of match score |
| `formula_version` | `text` | Formula version identifier |
| `calculated_at` | `timestamptz` | Calculation timestamp |

---

## 🧪 Verification Commands

### 1. Test In-Memory RAG Framework:
```powershell
python backend/test_rag.py
```

### 2. Test Conversational Refinement & Candidate State:
```powershell
python backend/test_conversational_refinement.py
```

### 3. Test Planner-Executor Orchestration:
```powershell
python backend/test_planner_executor.py
```

### 4. Test Algorithmic Fairness Audit:
```powershell
python backend/test_fairness.py
```

### 5. Verify Frontend Compilation:
```powershell
npm --prefix frontend run build
```
