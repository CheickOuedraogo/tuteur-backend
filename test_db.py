import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

db_url = os.getenv("DATABASE_URL")
print(f"Testing connection to: {db_url.split('@')[-1]}") # Hide password

try:
    conn = psycopg2.connect(db_url)
    print("SUCCESS: Connected to database!")
    conn.close()
except Exception as e:
    print(f"ERROR: {e}")
