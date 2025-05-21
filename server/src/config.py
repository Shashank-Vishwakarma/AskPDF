from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET_KEY: str
    
    # Supabase
    SUPABASE_URL: str
    SUPABASE_KEY: str

    # Groq
    GROQ_API_KEY: str
    
    # Qdrant
    QDRANT_HOST: str
    QDRANT_PORT: int
    TRANSFORMER_MODEL: str

    # Celery
    REDIS_URL: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

Config = Settings()