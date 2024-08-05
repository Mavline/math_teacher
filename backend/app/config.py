import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    assert OPENAI_API_KEY, "OPENAI_API_KEY must be set in .env file"


settings = Settings()
