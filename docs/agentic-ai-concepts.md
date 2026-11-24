# Agentic AI Concepts & Architecture in SkillSetu

This document explains the core **Agentic AI design patterns, architectural paradigms, and execution workflows** implemented across the SkillSetu platform.

---

## 1. Executive Summary

Traditional AI applications typically rely on single-prompt interactions: a prompt is submitted, and the model attempts to generate the entire answer in a single forward pass. This approach is prone to hallucinations, lacks deterministic tool guarantees, and fails on complex multi-step workflows.

SkillSetu adopts an **autonomous multi-agent architecture** that decouples high-level reasoning from deterministic execution. By combining **planning**, **shared state management**, **reflective self-correction**, **domain grounding**, and **tool dispatch**, the system operates as a reliable, auditable career workflow copilot.

---

## 2. Core Agentic AI Concepts Implemented

```text
                               +--------------------------------------------------------+
                               |                      User Request                      |
                               | "Analyze my resume, match remote frontend internships, |
                               |          and plan my learning roadmap"                 |
                               +--------------------------------------------------------+
                                                          |
                                                          v
                                       +--------------------------------------+
                                       |        Planner Agent (planner.py)    |
                                       |  [Concept 1: Task Decomposition]     |
                                       | Decomposes goal into structured plan |
                                       | using strictly allowed capabilities: |
                                       | ["profile", "retrieve", "match",     |
                                       |  "roadmap"]                          |
                                       +--------------------------------------+
                                                          |
                                                          v
                                       +--------------------------------------+
                                       |      Executor Agent (executor.py)    |
                                       | [Concept 2: Shared State Machine]    |
                                       |   Maintains dynamic AgentState       |
                                       +--------------------------------------+
                                                          |
                 +----------------------+-----------------+---------------------+
                 |                      |                 |                     |
                 v                      v                 v                     v
          [1. step_profile]     [2. step_retrieve]   [3. step_match]     [4. step_roadmap]
          Extracts candidate    Queries active       RAG-grounded match  Synthesizes 4-stage
          skills from resume    opportunity pool     scoring + saves     milestone roadmap
                                                     candidate state     to bridge gaps
                 |                      |                 |                     |
                 +----------------------+-----------------+---------------------+
                                                          |
                                                          v
                               +--------------------------------------------------------+
                               |                 Guardrails & Feedback                  |
                               | [Concept 3: Self-Correction & Reflection Loop]         |
                               | [Concept 4: Deterministic Tool Calling]                |
                               | [Concept 5: In-Memory RAG Grounding]                   |
                               | [Concept 6: Mixed-Initiative Conversational Loop]      |
                               +--------------------------------------------------------+
```

---

### Concept 1: Planner-Executor Pattern (Task Decomposition & Orchestration)
* **Code Reference:** [backend/app/agents/planner.py](file:///d:/SkillSetu/backend/app/agents/planner.py), [backend/app/agents/executor.py](file:///d:/SkillSetu/backend/app/agents/executor.py)
* **Design Principle:** Separate strategic reasoning from mechanical execution.
* **How It Works:**
  1. The **Planner Agent** receives high-level, open-ended instructions (e.g. *"Analyze my uploaded resume, find relevant Bangalore roles, and tell me how to prepare"*).
  2. The LLM acts as a meta-controller: it decomposes the goal into a directed sequence of discrete actions chosen strictly from a fixed capability whitelist: `["profile", "retrieve", "match", "roadmap"]`.
  3. The **Executor Agent** executes the plan deterministically using a step dispatch table (`STEP_DISPATCH`), eliminating unpredictable execution behavior.

---

### Concept 2: Shared State Machine (Agent State Pattern)
* **Code Reference:** `AgentState` class in [backend/app/agents/executor.py](file:///d:/SkillSetu/backend/app/agents/executor.py)
* **Design Principle:** Maintain persistent, evolving context across independent step boundaries.
* **How It Works:**
  * Instead of passing brittle text prompts between stages, a centralized `AgentState` object holds verified artifacts:
    * `profile`: Structured skills, projects, and educational background.
    * `student_skills`: Canonicalized skill set extracted from the candidate.
    * `retrieved_jobs_count`: Active opportunities available for evaluation.
    * `matches`: Scored and ranked job opportunities with gap bridges.
    * `roadmap`: Formulated milestone progression for skill acquisition.
    * `execution_trace`: Step-by-step latency, timestamp, and status telemetry.
  * Each execution step mutates the shared state and passes it to the next step.

---

### Concept 3: Self-Correction & Reflection Loop (Validation Guardrails)
* **Code Reference:** [backend/app/services/llm_validator.py](file:///d:/SkillSetu/backend/app/services/llm_validator.py)
* **Design Principle:** Robust agents must detect and recover from their own errors without crashing.
* **How It Works:**
  1. All LLM calls pass through `call_llm_with_validation()`.
  2. The LLM output is parsed against strict Pydantic schemas (`StudentProfile`, `ExtractedOpportunity`, `PreferenceUpdate`, `AgentPlan`).
  3. If parsing fails or schema validation fails (e.g., missing mandatory field or incorrect type), the validator captures the exact error trace.
  4. The engine executes an automated **reflection loop**: it sends the erroneous output and validation error back to the model as feedback:
     > *"Your previous response failed Pydantic validation: {error}. Please correct the fields and output valid JSON."*
  5. The model corrects its own output in a second turn, ensuring runtime resilience.

---

### Concept 4: Deterministic Tool Calling & Execution
* **Code Reference:** [backend/app/services/opportunity_matching.py](file:///d:/SkillSetu/backend/app/services/opportunity_matching.py), [backend/app/services/candidate_state_persistence.py](file:///d:/SkillSetu/backend/app/services/candidate_state_persistence.py)
* **Design Principle:** Do not let LLMs perform mathematical calculations, sorting, or direct database operations.
* **How It Works:**
  * The LLM reasons about *what* to do; deterministic Python code performs *how* it is done:
    * Matching scores are computed using an exact mathematical formula:
      $$\text{Score} = (0.80 \times \text{Skill Coverage}) + (0.10 \times \text{Location Score}) + (0.10 \times \text{Type Score})$$
    * Candidate match states are saved to PostgreSQL via Supabase client functions.
    * Set intersections and skill difference operations are performed deterministically in memory.

---

### Concept 5: Domain-Grounded RAG (In-Memory Semantic Anchoring)
* **Code Reference:** [backend/app/services/skill_framework_rag.py](file:///d:/SkillSetu/backend/app/services/skill_framework_rag.py)
* **Design Principle:** Prevent hallucinations and vocabulary drift by anchoring the agent in a verified knowledge taxonomy.
* **How It Works:**
  * Operates over a curated taxonomy of **232 entries** (8 industry roles, 224 tech skills).
  * Uses `all-MiniLM-L6-v2` ONNX embeddings via NumPy matrix dot product (`skill_embeddings.npy` of shape `(232, 384)`).
  * Anchors the workflow in three ways:
    1. **Skill Normalization:** Maps inconsistent inputs (`"ReactJS"`, `"react.js"`) to canonical names (`"React"`).
    2. **Skill Gap Bridging:** When a candidate lacks `"Docker"`, RAG fetches related competencies (`['Linux', 'Kubernetes', 'CI/CD', 'Microservices']`).
    3. **Prompt Grounding:** Injects framework documents into Groq prompts so extraction remains strictly grounded in real-world technologies.

---

### Concept 6: Mixed-Initiative Conversational Refinement (Human-in-the-Loop)
* **Code Reference:** [backend/app/agents/chat_agent.py](file:///d:/SkillSetu/backend/app/agents/chat_agent.py), [frontend/src/pages/Assistant.jsx](file:///d:/SkillSetu/frontend/src/pages/Assistant.jsx)
* **Design Principle:** Allow autonomous systems to be steered through natural conversation without losing prior state.
* **How It Works:**
  * When a user provides natural feedback in chat (*"Focus on remote roles in Bangalore with React"*):
    1. The Chat Agent extracts a structured delta (`PreferenceUpdate`).
    2. Merges this delta with the candidate's existing `student_preferences`.
    3. Re-triggers the deterministic matcher to refresh recommendations.
    4. Persists the new candidate state in `opportunity_matches`.
    5. Returns an explanatory conversational reply alongside live-updated job cards.

---

## 3. Code-to-Concept Mapping

| Agentic Concept | Primary File(s) | Function / Class |
| :--- | :--- | :--- |
| **Planner Decomposition** | `backend/app/agents/planner.py` | `generate_agent_plan()` |
| **State Machine Execution** | `backend/app/agents/executor.py` | `AgentState`, `execute_plan()`, `STEP_DISPATCH` |
| **Reflective Self-Correction** | `backend/app/services/llm_validator.py` | `call_llm_with_validation()` |
| **In-Memory RAG Grounding** | `backend/app/services/skill_framework_rag.py` | `SkillFrameworkEngine`, `normalize_skill()`, `get_related_skills()` |
| **Candidate State Store** | `backend/app/services/candidate_state_persistence.py` | `save_opportunity_matches()`, `save_student_preferences()` |
| **Conversational Refinement**| `backend/app/agents/chat_agent.py` | `parse_conversational_preference()` |
| **Orchestration API** | `backend/app/main.py` | `POST /api/agent/run`, `POST /api/chat` |

---

## 4. How to Explain This in an Interview or Presentation

When presenting the architecture, use this concise summary:

> *"Instead of building a simple prompt wrapper, we implemented an autonomous **Planner-Executor Agentic Architecture**. The **Planner Agent** uses Groq to decompose high-level candidate objectives into a structured sequence of capabilities (`profile`, `retrieve`, `match`, `roadmap`). An **Executor State Machine** executes these steps deterministically using Python tools, maintaining a shared **AgentState** object.*
>
> *To guarantee reliability, we added three core guardrails: an **automated reflection retry loop** that catches and fixes schema validation errors on the fly, an **in-memory RAG engine** using ONNX MiniLM vector embeddings for canonical skill normalization, and **candidate state persistence** that enables sub-50ms reloading and conversational filter refinement."*
