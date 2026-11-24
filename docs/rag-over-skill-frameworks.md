# In-Memory RAG Over Skill Frameworks

## 1. Overview & Architecture

SkillSetu implements an **in-memory hybrid Retrieval-Augmented Generation (RAG)** service built over a curated 232-document industry skill and role taxonomy.

The system replaces external vector databases (such as `pgvector`, Pinecone, or Weaviate) with an in-memory dense vector matrix stored as a NumPy array (`float32`), paired with a lightweight ONNX runtime execution of `sentence-transformers/all-MiniLM-L6-v2`.

```text
                               +---------------------------------------------+
                               |     skill_framework.json (232 records)      |
                               |    (8 industry roles, 224 tech skills)      |
                               +---------------------------------------------+
                                                      |
                                          Precompute & L2-Normalize
                                                      v
                               +---------------------------------------------+
                               |        skill_embeddings.npy (232 x 384)     |
                               |          Kept In-Memory via NumPy           |
                               +---------------------------------------------+
                                                      ^
                                                      | Cosine Similarity (Dot Product)
                                                      | Sub-millisecond Execution
                                                      v
+-----------------------+      ONNX runtime     +----------------------------+
| Raw Query / Resume /  | --------------------> | Query Embedding (1 x 384)  |
| Skill / Job listing   |   all-MiniLM-L6-v2    +----------------------------+
+-----------------------+                                     |
           |                                                  v
           | Lexical / Alias Boost                +--------------------------+
           +------------------------------------> | Hybrid Reranker          |
                                                  +--------------------------+
                                                              |
                 +--------------------------------------------+--------------------------------------------+
                 v                                            v                                            v
     [Skill Normalization]                         [Skill Gap Bridging]                       [LLM Prompt Grounding]
   "ReactJS"    -> "React"                  Missing "Docker" -> ["Linux",                Context injected into Groq
   "postgres db"-> "PostgreSQL"              "Kubernetes", "CI/CD", "Microservices"]      prompt to prevent hallucinations
   "k8s"        -> "Kubernetes"
```

---

## 2. Key Capabilities

### A. Canonical Skill Normalization
Different candidates, job postings, and APIs describe the same skill in varying ways. The RAG engine normalizes skill strings into a consistent project-controlled vocabulary:
- **Two-tier resolution:**
  1. **Tier 1 (Fast O(1) Alias Lookup):** Matches exact strings against curated aliases (e.g., `"reactjs"` $\rightarrow$ `"React"`, `"k8s"` $\rightarrow$ `"Kubernetes"`, `"ts"` $\rightarrow$ `"TypeScript"`).
  2. **Tier 2 (Vector Semantic Search):** Unseen or noisy variants (e.g., `"amazon web services"`, `"fast api framework"`, `"postgres db"`) are encoded via `all-MiniLM-L6-v2` and matched against the in-memory embedding matrix with a similarity threshold of $\ge 0.58$.

### B. Skill Gap Bridging
When matching a student against a job requirement, the matcher identifies missing skills and fetches related competencies and prerequisites:
- Missing **`Docker`** $\rightarrow$ Recommends `['Linux', 'Kubernetes', 'CI/CD', 'Microservices']`
- Missing **`React`** $\rightarrow$ Recommends `['JavaScript', 'HTML5', 'CSS3', 'TypeScript']`
- Missing **`Apache Kafka`** $\rightarrow$ Recommends `['Distributed Systems', 'Message Queues', 'Microservices', 'Event-Driven Architecture']`

### C. Grounded Prompt Context Generation
When analyzing resumes or extracting job requirements, `build_framework_context(query, limit=6)` formats top matching role and skill records into the LLM system prompt. This ensures:
- The LLM canonicalizes skills against known definitions.
- The LLM respects role-specific learning orders and prerequisites.
- The LLM does not hallucinate fictional technologies or qualifications.

---

## 3. Knowledge Base Specification

- **Framework Corpus:** `backend/app/data/skill_framework.json`
- **Embedding Matrix:** `backend/app/data/skill_embeddings.npy`
- **Metadata Index:** `backend/app/data/skill_metadata.json`
- **Total Entities:** 232 documents (8 industry roles, 224 granular skills)

### Taxonomy Schema

#### Role Document
```json
{
  "id": "role-full-stack-developer",
  "type": "role",
  "title": "Full-Stack Developer",
  "aliases": ["fullstack developer", "web developer", "mern developer"],
  "skills": ["JavaScript", "TypeScript", "React", "Next.js", "Node.js", "Express.js", "MongoDB", "PostgreSQL", "Docker", "REST API", "Tailwind CSS"],
  "description": "Builds complete web applications end-to-end, from responsive UI interfaces to backend microservices, databases, authentication, and deployments.",
  "learning_order": ["HTML5", "CSS3", "JavaScript", "TypeScript", "React", "Node.js", "Express.js", "REST API", "PostgreSQL", "Docker"]
}
```

#### Skill Document
```json
{
  "id": "skill-react",
  "type": "skill",
  "title": "React",
  "name": "React",
  "category": "Frontend Development",
  "aliases": ["reactjs", "react.js", "react js"],
  "skills": ["React"],
  "related_skills": ["JavaScript", "TypeScript", "Next.js", "Redux", "Tailwind CSS"],
  "prerequisites": ["JavaScript", "HTML5", "CSS3"],
  "description": "Declarative, component-based JavaScript library developed by Meta for building dynamic user interfaces."
}
```

---

## 4. API Reference

### 1. Hybrid Search
**Endpoint:** `GET /api/skill-framework/search`
- **Query Params:**
  - `query` (string, min 2 chars): Search query (e.g. `"pytorch deep learning"` or `"react developer"`).
  - `limit` (int, default 5, max 20): Maximum results to return.
- **Sample Request:**
  ```bash
  curl "http://localhost:8000/api/skill-framework/search?query=react%20developer&limit=3"
  ```
- **Sample Response:**
  ```json
  {
    "framework_version": "skillsetu-skill-framework-v2-comprehensive",
    "query": "react developer",
    "count": 3,
    "documents": [
      {
        "id": "role-frontend-developer",
        "type": "role",
        "title": "Frontend Developer",
        "category": "Engineering Roles",
        "description": "Specializes in building modern, responsive, high-performance web user interfaces..."
      },
      {
        "id": "skill-react",
        "type": "skill",
        "title": "React",
        "category": "Frontend Development",
        "description": "Declarative, component-based JavaScript library developed by Meta..."
      }
    ]
  }
  ```

### 2. Skill Normalization
**Endpoint:** `GET /api/skill-framework/normalize`
- **Query Params:**
  - `skill` (string): Raw or informal skill name.
- **Sample Request:**
  ```bash
  curl "http://localhost:8000/api/skill-framework/normalize?skill=reactjs"
  ```
- **Sample Response:**
  ```json
  {
    "raw": "reactjs",
    "canonical": "React",
    "is_normalized": true
  }
  ```

### 3. Skill Gap Bridging
**Endpoint:** `GET /api/skill-framework/gaps`
- **Query Params:**
  - `skill` (string): Missing skill requirement.
  - `limit` (int, default 4): Number of bridging recommendations.
- **Sample Request:**
  ```bash
  curl "http://localhost:8000/api/skill-framework/gaps?skill=Docker"
  ```
- **Sample Response:**
  ```json
  {
    "skill": "Docker",
    "canonical": "Docker",
    "related_bridging_skills": [
      "Linux",
      "Kubernetes",
      "CI/CD",
      "Microservices"
    ]
  }
  ```

---

## 5. How to Test the RAG Framework

### Method 1: Run the Automated Verification Suite
We have provided an automated test runner: [backend/test_rag.py](file:///d:/SkillSetu/backend/test_rag.py).

Run the suite from the project root:
```powershell
python backend/test_rag.py
```

The script runs 6 test modules:
1. **Engine Initialization:** Verifies that the corpus (232 documents) and embedding matrix `(232, 384)` load cleanly.
2. **Skill Normalization:** Validates 12 normalization cases (`ReactJS` $\rightarrow$ `React`, `postgres db` $\rightarrow$ `PostgreSQL`, `k8s` $\rightarrow$ `Kubernetes`, `py` $\rightarrow$ `Python`, etc.).
3. **Skill Gap Bridging:** Verifies related skill retrieval for missing competencies (`Docker`, `Kubernetes`, `React`, `Apache Kafka`, `FastAPI`).
4. **Hybrid Search:** Evaluates ranking accuracy across multi-word queries.
5. **Prompt Context Formatting:** Verifies context injection string for Groq prompts.
6. **Latency & Throughput Benchmark:** Runs 100 sequential queries and reports average latency (typically ~25-30ms per query on CPU).

---

### Method 2: Test via Python REPL
Run Python from your terminal:
```python
from backend.app.services.skill_framework_rag import (
    normalize_skill,
    get_related_skills,
    build_framework_context,
    search_skill_framework,
)

# 1. Normalization
print(normalize_skill("ReactJS"))       # Outputs: "React"
print(normalize_skill("postgres db"))   # Outputs: "PostgreSQL"
print(normalize_skill("k8s"))           # Outputs: "Kubernetes"
print(normalize_skill("amazon web services")) # Outputs: "AWS"

# 2. Skill Gap Bridging
print(get_related_skills("Docker"))     # Outputs: ['Linux', 'Kubernetes', 'CI/CD', 'Microservices']

# 3. Search
results = search_skill_framework("pytorch deep learning", limit=2)
for doc in results["documents"]:
    print(doc["title"], "-", doc["category"])
```

---

### Method 3: Test via HTTP Endpoints (When Backend is Running)
Start the FastAPI server:
```powershell
cd d:\SkillSetu\backend
uvicorn app.main:app --reload --port 8000
```

Then in another terminal or browser:
- **Search:** `http://localhost:8000/api/skill-framework/search?query=react&limit=3`
- **Normalize:** `http://localhost:8000/api/skill-framework/normalize?skill=reactjs`
- **Normalize (alias):** `http://localhost:8000/api/skill-framework/normalize?skill=k8s`
- **Skill Gaps:** `http://localhost:8000/api/skill-framework/gaps?skill=Kubernetes`

---

### Method 4: Test Integration with Job Matching
The RAG framework is wired directly into the job matching engine:
1. When a student resume has `"ReactJS"` and a job requires `"React"`, the matcher normalizes both to `"React"`, ensuring a 100% skill match instead of a false negative.
2. When a job requires `"Docker"` and the student lacks it, the matcher includes `related_gap_skills` in the response payload:
```json
{
  "job_id": "...",
  "title": "Software Engineer",
  "match_score": 85.0,
  "matched_skills": ["Python", "FastAPI"],
  "missing_skills": ["Docker"],
  "related_gap_skills": {
    "Docker": ["Linux", "Kubernetes", "CI/CD", "Microservices"]
  }
}
```
