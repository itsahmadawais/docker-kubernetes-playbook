import os

db_host = os.getenv("DB_HOST", "localhost")

print(f"Connecting to database at: {db_host}")