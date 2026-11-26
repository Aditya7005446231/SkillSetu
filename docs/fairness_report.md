# Synthetic Fairness & Demographic Invariance Test Report

**Test Execution Date:** `2026-11-24 17:34:35 UTC`  
**System Evaluated:** SkillSetu Deterministic Matching Formula  
**Test Harness:** `backend/test_fairness.py`  
**Result:** 🟢 **Δ = 0.00 across synthetic test cohort**

---

## 1. Scope and Limitations (What This Test Does and Does Not Show)

### What This Test Shows:
- The deterministic scoring function in `backend/test_fairness.py` computes identical scores for synthetic candidate records that share identical technical skills, regardless of the text values in candidate name or university fields.
- The matching formula directly consumes skill strings, location, and job type without weighting institution name or applicant identity.

### What This Test Does NOT Show:
- **No Production Pipeline Guarantee:** This test runs against synthetic fixture data directly invoking a standalone formula script; it does not exercise live PDF text extraction, LLM resume profiling, or the full production API path.
- **No Upstream LLM Bias Evaluation:** If an upstream LLM extracts different skills from different real-world resumes due to phrasing, demographic associations, or formatting differences, that variance is not tested here.
- **No Real-World Demographic Audit:** This test does not evaluate real applicant populations, outcome distributions, or statistical disparate impact over real hiring cycles.
- **No Legal or Regulatory Compliance:** This test does not constitute a formal audit for, nor certification under, US EEOC Uniform Guidelines, the EU Artificial Intelligence Act, or any other statutory employment law framework.

---

## 2. Synthetic Test Cohort

The test cohort consists of three synthetic candidate records constructed with **identical skill lists** and varying non-evaluated metadata fields:

| Candidate ID | Synthetic Name | Gender Proxy | Educational Institution | Institution Tier | Technical Skills |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `cand-001` | **Rahul Sharma** | Male | Indian Institute of Technology (IIT) Bombay | Tier-1 | `Python, FastAPI, React, TypeScript...` |
| `cand-002` | **Priya Patel** | Female | Government Engineering College, Bilaspur | Tier-3 | `Python, FastAPI, React, TypeScript...` |
| `cand-003` | **Mohammed Zeeshan** | Minority / Male | Aligarh Muslim University | Central University | `Python, FastAPI, React, TypeScript...` |

---

## 3. Test Results on Synthetic Job Requirements

| Opportunity Title | Company | Rahul Sharma (IIT Bombay) | Priya Patel (Tier-3 Rural) | Mohammed Zeeshan (Central Univ) | Score Delta (Δ) | Result |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Full-Stack Developer Intern** | CloudScale Systems | **100.0%** | **100.0%** | **100.0%** | `0.0` | 🟢 PASS |
| **Junior Software Engineer** | Nexus Technologies | **84.0%** | **84.0%** | **84.0%** | `0.0` | 🟢 PASS |
| **Frontend Engineer** | Innovate UI Labs | **60.0%** | **60.0%** | **60.0%** | `0.0` | 🟢 PASS |
| **Backend AI Developer** | Cognitive AI | **68.0%** | **68.0%** | **68.0%** | `0.0` | 🟢 PASS |

---

## 4. Observations

1. In this unit test, score variation between identical skill lists was zero ($\Delta = 0.0$), confirming that non-skill demographic fields do not enter the mathematical scoring formula.
2. Gap bridging logic returned identical prerequisite lists for all candidates when given identical missing skills.
