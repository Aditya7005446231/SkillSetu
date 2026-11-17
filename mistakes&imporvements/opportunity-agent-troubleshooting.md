# Opportunity Agent: Mistakes and Improvements

This document records the errors encountered while building and testing the
opportunity-fetching agent, along with their root causes and fixes.

## 1. Invalid provider board tokens

### Error

The synchronization request returned an upstream `404` for an Ashby URL using
the placeholder board token `company-three`.

### Root cause

The initial implementation used Greenhouse, Lever, and Ashby board adapters.
Placeholder board tokens remained in the local environment configuration.

### Fix

- Removed Greenhouse, Lever, and Ashby from the opportunity source flow.
- Replaced them with the OpenWeb Ninja JSearch API.
- Removed the obsolete source adapters and environment variables.

### Improvement

Validate provider credentials and source identifiers before starting a sync.
Never use example tokens in an active local configuration.

## 2. JSearch response shape mismatch

### Error

The adapter raised:

```text
'str' object has no attribute 'get'
```

### Root cause

The API response stores jobs under `data.jobs`, while the adapter initially
treated `data` itself as a list. Some `job_apply_links` values can also be
strings instead of objects.

### Fix

- Read jobs from `payload["data"]["jobs"]`.
- Accept both string and object forms for application links.
- Skip listings without a title, description, or application URL.

### Improvement

Inspect and validate external API response shapes before mapping them into
internal schemas. Keep the adapter tolerant of documented response variants.

## 3. Local TLS certificate verification failure

### Error

The JSearch request returned:

```text
CERTIFICATE_VERIFY_FAILED: self-signed certificate in certificate chain
```

### Root cause

The local Python HTTP environment did not use a CA bundle trusted by the
network connection.

### Fix

- Configured the JSearch `httpx.AsyncClient` with the `certifi` CA bundle.
- Added `certifi` to backend requirements.
- Kept TLS verification enabled; it was not disabled as a workaround.

### Improvement

Use an explicit trusted CA bundle for outbound API clients and test TLS
connectivity separately from API authentication.

## 4. Stale backend process after code changes

### Error

Swagger continued returning the previous TLS-related `502` after the adapter
had already been fixed.

### Root cause

The running Uvicorn process had not loaded the latest source changes.

### Fix

Stopped the old process when necessary and restarted Uvicorn from the project
root:

```powershell
cd D:\SkillSetu
python -m uvicorn backend.app.main:app --reload
```

### Improvement

After backend changes, verify the active process and restart it before testing.
Check `http://127.0.0.1:8000/docs` to confirm the server is available.

## 5. Supabase `maybe_single()` returned `None`

### Error

The first synchronization returned:

```text
'NoneType' object has no attribute 'data'
```

### Root cause

Supabase returns `None` from `maybe_single().execute()` when no matching job
exists. The persistence code assumed a response object always existed.

### Fix

The persistence layer now safely handles both cases:

- An existing response with `.data`
- No matching response represented by `None`

### Improvement

Treat “no existing row” as a normal branch when using `maybe_single()`.
Database persistence code should validate response objects before accessing
their fields.

## 6. Groq DNS/network connection failure

### Error

The full synchronization failed with:

```text
groq.APIConnectionError: Connection error
[Errno 11001] getaddrinfo failed
```

### Root cause

The local machine temporarily failed to resolve or connect to the Groq API
hostname.

### Fix

Verified DNS and port connectivity with:

```powershell
nslookup api.groq.com
Test-NetConnection api.groq.com -Port 443
```

Then verified the Groq API using the backend environment configuration. The
Groq API connection succeeded.

### Improvement

Separate network failures from API-key failures. Add bounded retries and
clear error messages around external AI calls before production use.

## 7. Environment variables in standalone tests

### Error

A standalone Groq test reported that `GROQ_API_KEY` was missing even though
the backend had the key configured.

### Root cause

Running `python` from the repository root does not automatically load
`backend/.env`.

### Fix

The test explicitly loaded the backend environment file before creating the
Groq client.

### Improvement

Use the application settings/configuration loader for diagnostic scripts
instead of reading environment variables directly.

## Current verified state

- OpenWeb Ninja JSearch is configured for India with default query
  `software developer internship`.
- JSearch returned India-relevant results successfully.
- Backend Python compilation passed.
- Groq connectivity was verified successfully.
- Missing Supabase rows are handled correctly.
- API keys and service credentials are not documented in this file.

