import tomlkit
from pydantic import BaseModel, BaseSettings


def read_conf_file(_: BaseSettings):
    with open("config.toml", "rb") as f:
        return tomlkit.load(f)


class Config(BaseSettings):
    code_folder: str

    class Config:
        env_prefix = 'KAPPA_FN_CODE_'

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
