from dotenv import load_dotenv
import os
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
cred = credentials.Certificate("googleServiceAccount.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
