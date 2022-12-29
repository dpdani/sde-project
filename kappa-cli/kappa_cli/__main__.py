import getpass
from pathlib import Path

import halo
import typer

import kappa_client.apis.tags.default_api
from kappa_client.model.create_function import CreateFunction
from .config import config


cli = typer.Typer()

KappaApi = kappa_client.apis.tags.default_api.DefaultApi

conf = kappa_client.Configuration(config.kappa)
api_client = kappa_client.ApiClient(conf)
kappa = KappaApi(api_client)


def error(message):
    typer.secho(message, fg="red")
    exit(1)


@cli.command()
def signup():
    username = typer.prompt("Choose a username")
    password = getpass.getpass("Choose a password: ")
    password_check = getpass.getpass("Enter your password again: ")
    if password != password_check:
        error("Passwords do not match.")
    response = kappa.signup(query_params={
        "username": username,
        "password": password,
    }).body
    print(response)

fn = typer.Typer()
cli.add_typer(fn, name="fn")

@fn.command()
def create(name: str, code: Path = typer.Argument(..., exists=True, file_okay=True, dir_okay=False, readable=True)):
    with open(code, 'r') as f:
        code = f.read()
    with halo.Halo(text=f"Creating '{name}'...", spinner="dots"):
        kappa.create_function(CreateFunction(name=name, code=code))
