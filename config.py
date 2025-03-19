# config.py
import os
from dotenv import load_dotenv

load_dotenv()  # If you're using a .env file

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
NYLAS_API_KEY = os.getenv("NYLAS_API_KEY", "")
NYLAS_API_URI = os.getenv("NYLAS_API_URI", "")
NYLAS_GRANT_ID = os.getenv("NYLAS_GRANT_ID", "")

