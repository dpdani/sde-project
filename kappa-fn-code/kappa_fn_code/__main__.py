import subprocess

import typer

from kappa_fn_code import config


cli = typer.Typer()


@cli.command()
def start():
    subprocess.call(
        f"uvicorn kappa_fn_code.__init__:app "
        f"--host {config.server.host} "
        f"--port {config.server.port} ",
        shell=True
    )
