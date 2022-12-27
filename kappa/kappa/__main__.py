import subprocess

import typer

from kappa.config import config


cli = typer.Typer()


@cli.command()
def start():
    subprocess.call(
        "uvicorn kappa.__init__:app "
        f"--host {config.server.host} "
        f"--port {config.server.port} ",
        shell=True
    )
