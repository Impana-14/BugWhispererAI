import os

from dotenv import load_dotenv

load_dotenv()

APP_NAME = "BugWhisperer AI"
APP_VERSION = "1.0.0"

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")
