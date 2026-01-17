import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
    RAPIDAPI_HOST = "real-time-amazon-data.p.rapidapi.com"
    BASE_URL = f"https://{RAPIDAPI_HOST}"

settings = Settings()
