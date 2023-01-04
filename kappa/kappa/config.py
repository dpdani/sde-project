import tomllib

from pydantic import BaseModel, BaseSettings, Extra


def read_conf_file(_: BaseSettings):
    with open("kappa/config.toml", "rb") as f:
        return tomllib.load(f)


class Server(BaseModel):
    host: str
    port: int
    reload: bool


class Kappa(BaseModel):
    data: str
    fn_code: str
    logs: str
    runner: str


class GitHub(BaseModel):
    base_url: str
    api_version: str
    text: str


class Config(BaseSettings):
    server: Server
    kappa: Kappa
    github: GitHub

    class Config:
        env_prefix = 'KAPPA_'
        extra = Extra.ignore

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
