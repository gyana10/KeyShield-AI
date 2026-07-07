from dotenv import load_dotenv
import os

load_dotenv()

# JWT Configuration
SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "keyshield_super_secret_key_2026"
)

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 60