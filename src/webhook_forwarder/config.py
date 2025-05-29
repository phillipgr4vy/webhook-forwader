import os
from dotenv import load_dotenv

load_dotenv()

OAUTH_TOKEN_URL = os.getenv("OAUTH_TOKEN_URL")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
FORWARD_URL = os.getenv("FORWARD_URL")
