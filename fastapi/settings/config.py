import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings:
    # MongoDB Configuration
    MONGODB_URI: str = os.getenv(
        "MONGODB_URI", 
        "mongodb://localhost:27017/mcpmyapi"
    )
    
    # OpenAI Configuration
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    
    # Application Configuration
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

# Global settings instance
settings = Settings() 