import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
    RAPIDAPI_HOST = "real-time-amazon-data.p.rapidapi.com"
    BASE_URL = f"https://{RAPIDAPI_HOST}"

settings = Settings()

# Debug: verify key loading in Railway logs
if settings.RAPIDAPI_KEY:
    print(f"DEBUG: RAPIDAPI_KEY detected. Length: {len(settings.RAPIDAPI_KEY)}")
else:
    print("DEBUG: RAPIDAPI_KEY NOT FOUND in environment variables.")
