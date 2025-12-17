from pydantic_settings import BaseSettings


class Settings(BaseSettings):
  GROQ_API_KEY: str
  DEFAULT_LLM: str
  TEMPERATURE: float

  class Config:
    env_file = '.env'

settings = Settings() # type: ignore