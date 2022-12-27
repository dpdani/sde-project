import tomllib

from pydantic import BaseModel, BaseSettings, Extra


def read_conf_file(_: BaseSettings):
    with open("kappa/config.toml", "rb") as f:
        return tomllib.load(f)


class Server(BaseModel):
    host: str
    port: int


class Config(BaseSettings):
    server: Server

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
