import time
import uuid
from pprint import pprint

import requests
from fastapi import Depends, FastAPI, Request

import kappa_data_client
import kappa_data_client.apis.tags.default_api
import kappa_fn_code_client
import kappa_fn_code_client.apis.tags.default_api
import kappa_runner_client
import kappa_runner_client.apis.tags.default_api
from kappa.config import config
from kappa_data import LoginUser, User
from kappa_data.security import oauth2_scheme
from kappa_data_client.model.create_function import CreateFunction
from kappa_runner_client.model.function_to_load import FunctionToLoad


app = FastAPI(
    title="kappa",
    version="0.0.0",
    author="dpdani",
    generate_unique_id_function=lambda route: f"{route.name}",
)

KappaDataApi = kappa_data_client.apis.tags.default_api.DefaultApi
KappaCodeApi = kappa_fn_code_client.apis.tags.default_api.DefaultApi
KappaRunnerApi = kappa_runner_client.apis.tags.default_api.DefaultApi


def get_kappa_data(header_name: str | None = None, header_value: str | None = None) -> KappaDataApi:
    conf = kappa_data_client.Configuration(config.kappa.data)
    with kappa_data_client.ApiClient(conf, header_name, header_value) as api_client:
        kappa_data = KappaDataApi(api_client)
        yield kappa_data


def get_kappa_code() -> KappaCodeApi:
    conf = kappa_fn_code_client.Configuration(config.kappa.fn_code)
    with kappa_fn_code_client.ApiClient(conf) as api_client:
        kappa_code = KappaCodeApi(api_client)
        yield kappa_code


def get_kappa_runner() -> KappaRunnerApi:
    conf = kappa_runner_client.Configuration(config.kappa.runner)
    with kappa_runner_client.ApiClient(conf) as api_client:
        kappa_runner = KappaRunnerApi(api_client)
        yield kappa_runner


def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    kappa_data: KappaDataApi
    with get_kappa_data("Authorization", f"Bearer {token}") as kappa_data:
        return User.parse_obj(kappa_data.get_me().body.__dict__)


@app.post("/signup/")
def signup(user: LoginUser, kappa_data: KappaDataApi = Depends(get_kappa_data)):
    return kappa_data.signup(user).body

@app.post("/login/")
def login(user: LoginUser, kappa_data: KappaDataApi = Depends(get_kappa_data)):
    return kappa_data.login(user).body


@app.post("/functions/")
def create_function(name: str, code: str, user: User = Depends(get_current_user),
                    kappa_data: KappaDataApi = Depends(get_kappa_data),
                    kappa_code: KappaCodeApi = Depends(get_kappa_code),
                    kappa_runner: KappaRunnerApi = Depends(get_kappa_runner)):
    code_id = str(uuid.uuid4())
    kappa_code.create_code(
        path_params={
            "code_id": code_id,
        },
        body=code,
    )
    fn = kappa_data.create_function(CreateFunction(
        name=name,
        code_id=code_id,
    )).body
    kappa_runner.load_function(FunctionToLoad(fn_id=fn.fn_id, code_id=code_id))
    while not (can_run := kappa_runner.is_function_loaded(fn.fn_id).body).loaded:
        time.sleep(0.01)
    gh = requests.get(f"https://github.com/search/repositories?q={name}").json()
    pprint(gh)
    return can_run.fn


@app.get("/functions/{fn_name}")
def execute_function(fn_name: str, request: Request, user: User = Depends(get_current_user),
                     kappa_data: KappaDataApi = Depends(get_kappa_data),
                     kappa_runner: KappaRunnerApi = Depends(get_kappa_runner)):
    fn = kappa_data.get_function(path_params={"fn_name": fn_name}).body
    return kappa_runner.execute_function(fn.fn_id, arguments=request.query_params)


@app.delete("/functions/{fn_name}")
def delete_function(fn_name: str, user: User = Depends(get_current_user),
                    kappa_data: KappaDataApi = Depends(get_kappa_data),
                    kappa_code: KappaCodeApi = Depends(get_kappa_code),
                    kappa_runner: KappaRunnerApi = Depends(get_kappa_runner)):
    fn = kappa_data.get_function(path_params={"fn_name": fn_name}).body
    kappa_code.delete_code(path_params={
        "code_id": fn_name,
    })
    kappa_data.delete_function(path_params={
        "fn_name": fn_name,
    })
    kappa_runner.unload_function(fn.fn_id)
    while kappa_runner.is_function_loaded(fn.fn_id).body.loaded:
        time.sleep(0.01)
