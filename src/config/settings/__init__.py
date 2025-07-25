import os
from pathlib import Path

from dotenv import load_dotenv

env = os.getenv("DJANGO_ENV", "development")
if env == "production":
    from .production import *
else:
    _BASE_DIR = Path(__file__).resolve().parent.parent.parent
    load_dotenv(_BASE_DIR.parent / ".env")
    from .development import *
