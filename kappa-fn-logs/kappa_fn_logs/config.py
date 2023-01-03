import tomllib
from pydantic import BaseModel, BaseSettings


def read_conf_file(_: BaseSettings):
    with open("kappa-fn-logs/config.toml", "rb") as f:
        return tomllib.load(f)


class Database(BaseModel):
    url: str
    database: str
    collection: str


class Server(BaseModel):
    host: str
    port: int


class Config(BaseSettings):
    db: Database
    server: Server

    class Config:
        env_prefix = 'KAPPA_FN_LOGS_'

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
