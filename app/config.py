from pydantic_settings import BaseSettings


class Config(BaseSettings):
    MAIN_URL:str
    TARGET_URL:str
    COUNT_THREADS:int
    CHUNK_SIZE:int

    PATH_SAVE:str

    MAX_QUALITY:str

    USER_AGENT:str

    class Config:
        env_file = '.env'


settings = Config()