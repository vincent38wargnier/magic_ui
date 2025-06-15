import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Settings:
    # MongoDB Configuration
    MONGODB_URI: str = os.getenv("MONGODB_URI", "mongodb://localhost:27017/mcpmyapi")

    # OpenAI Configuration
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")

    # Telegram Configuration
    TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "")

    # Application Configuration
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"


# Global settings instance
settings = Settings()
