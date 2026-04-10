import os
from dotenv import load_dotenv

try:
	from supabase import create_client, Client
except ImportError:
	create_client = None
	Client = None

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = None

if create_client and SUPABASE_URL and SUPABASE_KEY:
	try:
		supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
	except Exception:
		supabase = None
