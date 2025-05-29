import os

OAUTH_TOKEN_URL = os.getenv("OAUTH_TOKEN_URL")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
FORWARD_URL = os.getenv("FORWARD_URL")

# Optional: Raise if required vars are missing
required_vars = [OAUTH_TOKEN_URL, CLIENT_ID, CLIENT_SECRET, USERNAME, PASSWORD, FORWARD_URL]
if any(var is None for var in required_vars):
    raise RuntimeError("Missing one or more required environment variables.")