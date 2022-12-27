import subprocess

import typer

from kappa_data.config import config


cli = typer.Typer()


@cli.command()
def start():
    subprocess.call(
        "uvicorn kappa_data.__init__:app "
        f"--host {config.server.host} "
        f"--port {config.server.port} ",
        shell=True
    )
