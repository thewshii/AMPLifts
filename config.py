# config.py
import os
from dotenv import load_dotenv

load_dotenv()  # If you're using a .env file

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "AIzaSyBHGhLOxK9KKie74WmLsMOUeTNJXnmN1SQ")
NYLAS_API_KEY = os.getenv("NYLAS_API_KEY", "nyk_v0_7lILSOKilJIWm0V6H2tLQcfg9aMad0S6QBJsrHJ30KYne8237T9M6YoL0Pxg4KkO")
NYLAS_API_URI = os.getenv("NYLAS_API_URI", "https://api.us.nylas.com")
NYLAS_GRANT_ID = os.getenv("NYLAS_GRANT_ID", "4ef046e6-a8d7-4e3f-b71a-307abec9a01b")

