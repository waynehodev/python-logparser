from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    db_path: str = './db/securitylogs.db'

settings = Settings()