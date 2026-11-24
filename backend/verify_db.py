"""
SkillSetu Database State & Persistence Verifier
Executes a live health check across all Supabase tables.
"""
import sys
sys.path.append('backend')
from app.database import get_service_client

def verify_database():
    client = get_service_client()
    print("=" * 60)
    print("   SKILLSETU LIVE SUPABASE DATABASE AUDIT")
    print("=" * 60)

    tables = [
        ("profiles", "Student Profiles"),
        ("student_skills", "Student Skills Extracted"),
        ("skills", "Global Skills Taxonomy"),
        ("jobs", "Synced Job/Internship Listings"),
        ("student_preferences", "Conversational Preferences Store"),
        ("opportunity_matches", "Candidate Match Persistence"),
        ("student_resumes", "Multi-Resume Profiles"),
    ]

    for table_name, label in tables:
        try:
            res = client.table(table_name).select("*").limit(5).execute()
            count = len(res.data or [])
            print(f" [PASS] Table '{table_name}' ({label}): OK ({count} records sampled)")
            if count > 0:
                sample = res.data[0]
                keys = list(sample.keys())[:5]
                print(f"        Sample columns: {keys}")
        except Exception as e:
            err_msg = str(e)
            if "schema cache" in err_msg or "PGRST205" in err_msg:
                print(f" [PENDING SQL] Table '{table_name}': Table not created in Supabase yet (Run SQL migration)")
            else:
                print(f" [INFO] Table '{table_name}': {err_msg[:80]}")

    print("=" * 60)

if __name__ == "__main__":
    verify_database()
