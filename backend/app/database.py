import os
from pathlib import Path

from dotenv import load_dotenv
from supabase import Client, create_client

load_dotenv(Path(__file__).resolve().parents[1] / ".env")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SECRET_KEY") or os.getenv("SUPABASE_ANON_KEY")

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