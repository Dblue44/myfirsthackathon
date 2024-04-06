from pydantic_settings import BaseSettings


class BaseConfig(BaseSettings):
    class Config:
        env_file = "../.env"
        env_file_encoding = "utf-8"
        frozen = True
        env_nested_delimiter = '__'
        extra = "ignore"

    def __hash__(self) -> int:
        return hash(self.model_dump_json())


class Config(BaseConfig):
    token: str
