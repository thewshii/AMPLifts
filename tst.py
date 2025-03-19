from dotenv import load_dotenv
from config import NYLAS_API_KEY, NYLAS_API_URI, NYLAS_GRANT_ID
load_dotenv()

import os
import sys
from nylas import Client

nylas = Client(
    NYLAS_API_KEY,
    NYLAS_API_URI)


grant_id = NYLAS_GRANT_ID
calendars = nylas.calendars.list(grant_id)

print(calendars)