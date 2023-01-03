import typer
import uvicorn

from . import app
from .config import config


cli = typer.Typer()


@cli.command()
def start():
    return uvicorn.run(
        app,
        host=config.server.host,
        port=config.server.port,
    )


if __name__ == '__main__':
    cli()
