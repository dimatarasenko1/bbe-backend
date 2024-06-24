from dotenv import load_dotenv
import os
import json
import base64
import logging
from dataclasses import dataclass
import firebase_admin
from firebase_admin import credentials, firestore
from supabase import create_client, Client

load_dotenv()

# env
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


@dataclass(frozen=True)
class Settings:
    OPENAI_KEY: str = os.getenv("OPENAI_KEY")
    SUPABASE_URL: str = os.getenv("SUPABASE_URL")
    SUPABASE_KEY: str = os.getenv("SUPABASE_PRIVATE_KEY")


settings = Settings()

supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

# firebase
google_service_account_json_base64 = os.getenv("GOOGLE_SERVICE_ACCOUNT_ENCODED_JSON")
google_service_account_data = json.loads(
    base64.b64decode(google_service_account_json_base64)
)
cred = credentials.Certificate(google_service_account_data)
# cred = credentials.Certificate("googleServiceAccount.json")

firebase_admin.initialize_app(cred)
db = firestore.client()
