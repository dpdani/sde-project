import tomllib
from pydantic import BaseModel, BaseSettings


def read_conf_file(_: BaseSettings):
    with open("kappa-data/config.toml", "rb") as f:
        return tomllib.load(f)


class Database(BaseModel):
    url: str


class Server(BaseModel):
    host: str
    port: int
    reload: bool


class Config(BaseSettings):
    db: Database
    secret: str
    server: Server

    class Config:
        env_prefix = 'KAPPA_DATA_'

        @classmethod
        def customise_sources(
                cls,
                init_settings,
                env_settings,
                file_secret_settings,
        ):
            return (
                init_settings,
                read_conf_file,
                env_settings,
                file_secret_settings,
            )


config = Config()
