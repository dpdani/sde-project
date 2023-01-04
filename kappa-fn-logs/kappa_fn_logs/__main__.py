from pathlib import Path

import typer
import uvicorn

from .config import config


cli = typer.Typer()


@cli.command()
def start():
    return uvicorn.run(
        f"{__package__}.__init__:app",
        host=config.server.host,
        port=config.server.port,
        reload=config.server.reload,
        reload_delay=1,
        reload_dirs=[str(Path(__file__).parent.parent)],
    )


if __name__ == '__main__':
    cli()
