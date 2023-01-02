import tomllib

import tomlkit
from pydantic import BaseSettings


conf_path = "kappa-cli/config.toml"


def read_conf_file(_: BaseSettings):
    with open(conf_path, "rb") as f:
        return tomllib.load(f)


def write_conf_file():
    content = tomlkit.dumps(config.dict())
    with open(conf_path, 'w') as f:
        f.write(content)


class Config(BaseSettings):
    kappa: str
    username: str | None = None
    token: str | None = None

    class Config:
        env_prefix = 'KAPPA_CLI_'

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
