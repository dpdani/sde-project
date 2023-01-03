import getpass
import json
from pathlib import Path

import halo
import requests
from rich import print
import typer
from starlette import status

import kappa_client.apis.tags.default_api
from kappa_client import ApiException
from kappa_client.model.create_function import CreateFunction
from kappa_client.model.login_user import LoginUser
from .config import config, write_conf_file


cli = typer.Typer()

KappaApi = kappa_client.apis.tags.default_api.DefaultApi

conf = kappa_client.Configuration(config.kappa)
if config.token is None:
    api_client = kappa_client.ApiClient(conf)
else:
    api_client = kappa_client.ApiClient(conf, "Authorization", f"Bearer {config.token}")
kappa = KappaApi(api_client)


def error(message=None):
    if message is not None:
        print(f"[red]{message}[/red]")
    exit(1)


def assert_kappa_up():
    try:
        requests.get(config.kappa)
    except requests.ConnectionError:
        error(f"Kappa is not reachable at {config.kappa}")


def assert_logged_in():
    assert_kappa_up()
    if config.token is None:
        error("Please, login before running this command.")
    try:
        me = kappa.get_me().body
    except ApiException:
        return error("Token expired, please login again.")
    assert me["username"] == config.username


@cli.command()
def signup():
    assert_kappa_up()
    username = typer.prompt("Choose a username")
    password = getpass.getpass("Choose a password: ")
    password_check = getpass.getpass("Enter your password again: ")
    if password != password_check:
        error("Passwords do not match.")
    try:
        kappa.signup(LoginUser(
            username=username,
            password=password,
        ))
    except ApiException:
        error("Failed to create user.")
    print(f"[green]User {username} created[/green]")


@cli.command()
def login():
    assert_kappa_up()
    username = typer.prompt("Enter username")
    password = getpass.getpass("Enter password: ")
    with halo.Halo(text="Logging in...", spinner="dots") as spin:
        try:
            response = kappa.login(LoginUser(username=username, password=password)).body
        except ApiException:
            spin.fail("Authentication failed.")
            error()
        config.username = username
        config.token = str(response["access_token"])
        write_conf_file()
        spin.succeed("Logged in")


fn = typer.Typer()
cli.add_typer(fn, name="fn")


@fn.command()
def create(name: str, code: Path = typer.Argument(..., exists=True, file_okay=True, dir_okay=False, readable=True)):
    assert_logged_in()
    with open(code, 'r') as f:
        code = f.read()
    with halo.Halo(text=f"Creating '{name}'...", spinner="dots") as spin:
        try:
            response = kappa.create_function(CreateFunction(name=name, code=code)).body
        except ApiException as e:
            match e.status:
                case status.HTTP_409_CONFLICT:
                    spin.fail(f"Function '{name}' already exists.")
                case status.HTTP_406_NOT_ACCEPTABLE:
                    spin.fail(f"Code is not acceptable: {json.loads(e.body)['detail']}")
                case _:
                    raise e
        else:
            spin.succeed(f"Function {response['fn_name']} created")
            print(f"{response['related']['text']}")
            for repo in response['related']['repos']:
                print(repo)

@fn.command()
def delete(name: str):
    assert_logged_in()
    with halo.Halo(text=f"Deleting '{name}'...", spinner="dots") as spin:
        try:
            kappa.delete_function(path_params={"fn_name": name})
        except ApiException as e:
            match e.status:
                case status.HTTP_404_NOT_FOUND:
                    spin.fail(f"Function '{name}' not found")
                case _:
                    raise e
        else:
            spin.succeed(f"Function '{name}' deleted")


@fn.command(
    context_settings={"allow_extra_args": True, "ignore_unknown_options": True}
)
def execute(name: str, ctx: typer.Context):
    assert_logged_in()
    params = {}
    key = None
    for arg in ctx.args:
        if key is None:
            assert arg.startswith("--")
            key = arg.removeprefix("--")
        else:
            params[key] = arg
            key = None
    with halo.Halo(f"Executing function {name}...", spinner="dots") as spin:
        try:
            execution = kappa.execute_function(path_params={"fn_name": name}, query_params={"params": params}).body
        except ApiException as e:
            match e.status:
                case status.HTTP_400_BAD_REQUEST:
                    spin.fail()
                    error(f"Invalid argument: {json.loads(e.body)['detail']['invalid_argument']}")
                case status.HTTP_404_NOT_FOUND:
                    spin.fail()
                    error(f"Function {name} not found.")
                case _:
                    spin.fail()
                    raise e
        spin.succeed()
    print(f"Function '{name}' {execution['status']} with output:")
    print(dict(execution["output"]))
    print(f"See the logs of this execution by running: kappa-cli logs exec {execution['exec_id']}")


logs = typer.Typer()
cli.add_typer(logs, name="logs")

@logs.command(name="fn")
def fn_logs(name: str):
    assert_logged_in()
    with halo.Halo(f"Fetching logs for '{name}'...", spinner="dots") as spin:
        try:
            logs = kappa.get_fn_logs(path_params={"fn_name": name})
        except ApiException as e:
            match e.status:
                case status.HTTP_404_NOT_FOUND:
                    spin.fail()
                    error(f"Function '{name}' not found.")
                case _:
                    raise e
        spin.succeed()
        for log in logs.body["logs"]:
            print(f"{log['ts']} | {log['content']}")
