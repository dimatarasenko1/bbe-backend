from dotenv import load_dotenv
import os
import json
import base64
import logging
from dataclasses import dataclass
import firebase_admin
from firebase_admin import credentials, firestore, auth

load_dotenv()

# env
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


@dataclass(frozen=True)
class Settings:
    OPENAI_KEY: str = os.getenv("OPENAI_KEY")


settings = Settings()

# firebase
google_service_account_json_base64 = os.getenv("GOOGLE_SERVICE_ACCOUNT_ENCODED_JSON")
google_service_account_data = json.loads(
    base64.b64decode(google_service_account_json_base64)
)
cred = credentials.Certificate(google_service_account_data)
# cred = credentials.Certificate("googleServiceAccount.json")

firebase_admin.initialize_app(cred)
db = firestore.client()
