import tomllib
from pydantic import BaseModel, BaseSettings


def read_conf_file(_: BaseSettings):
    with open("kappa-logs/config.toml", "rb") as f:
        return tomllib.load(f)


class Kappa(BaseModel):
    data: str
    fn_logs: str


class Server(BaseModel):
    host: str
    port: int


class Config(BaseSettings):
    kappa: Kappa
    server: Server

    class Config:
        env_prefix = 'KAPPA_LOGS_'

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
