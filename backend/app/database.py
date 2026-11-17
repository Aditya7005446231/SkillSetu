import os
from pathlib import Path

from dotenv import load_dotenv
from supabase import Client, create_client

load_dotenv(Path(__file__).resolve().parents[1] / ".env")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SECRET_KEY") or os.getenv("SUPABASE_ANON_KEY")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError(
        "SUPABASE_URL and SUPABASE_SECRET_KEY (or SUPABASE_ANON_KEY) "
        "must be configured in the environment."
    )

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def get_authenticated_client(access_token: str) -> Client:
    """Create a Supabase client whose requests run as the authenticated user."""
    client = create_client(SUPABASE_URL, SUPABASE_KEY)
    client.postgrest.auth(access_token)
    return client


def get_service_client() -> Client:
    """Create the server-only client used by scheduled ingestion."""
    if not SUPABASE_SERVICE_ROLE_KEY:
        raise RuntimeError("SUPABASE_SERVICE_ROLE_KEY is required for scheduled sync.")
    return create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)