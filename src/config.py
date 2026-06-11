from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")
    database_url: str = Field(default="sqlite:///data/sample.db", env="DATABASE_URL")
    llm_model: str = Field(default="gpt-4o-mini", env="LLM_MODEL")
    max_retries: int = Field(default=3, env="MAX_RETRIES")

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
