import os

from dotenv import load_dotenv

# Loading from .env
load_dotenv()


class Config:
    SERPAPI_API_KEY: str | None = os.environ.get("SERPAPI_API_KEY")

    # Setting the exposed port (default to 5000)
    PORT: int = int(os.environ.get("PORT", 5000))

    # Expects "production" or "development" (default to "production")
    FLASK_ENV: str = os.environ.get("FLASK_ENV", "production")

    # Expects "INFO" or "DEBUG" (default into "INFO")
    LOG_LEVEL: str = os.environ.get("LOG_LEVEL", "INFO").upper()

    @classmethod
    def validate(cls) -> None:
        if not cls.SERPAPI_API_KEY and cls.FLASK_ENV != "testing":
            # We allow a missing key strictly in testing, but NEVER in development/production.
            raise ValueError("CRITICAL: SERPAPI_API_KEY is not set in the environment.")

        valid_log_levels = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        if cls.LOG_LEVEL not in valid_log_levels:
            cls.LOG_LEVEL = "INFO"
