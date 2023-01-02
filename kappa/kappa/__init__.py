import json
import time
import uuid
from pprint import pprint

import requests
from fastapi import Depends, FastAPI, HTTPException, Request
from pydantic import BaseModel
from starlette import status

import kappa_data_client
import kappa_data_client.apis.tags.default_api
import kappa_fn_code_client
import kappa_fn_code_client.apis.tags.default_api
import kappa_runner_client
import kappa_runner_client.apis.tags.default_api
from kappa.config import config
from kappa_data import LoginUser, User
from kappa_data.security import credentials_exception, oauth2_scheme
from kappa_data_client.model.create_function import CreateFunction as DataCreateFunction
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


def get_kappa_data(header_name: str | None = None, header_value: str | None = None):
    conf = kappa_data_client.Configuration(config.kappa.data)
    with kappa_data_client.ApiClient(conf, header_name, header_value) as api_client:
        kappa_data = KappaDataApi(api_client)
        if header_value is not None:
            try:
                kappa_data.get_me()
            except kappa_data_client.ApiException as e:
                raise credentials_exception from e
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


def get_auth_kappa_data(token: str = Depends(oauth2_scheme)) -> KappaDataApi:
    yield from get_kappa_data("Authorization", f"Bearer {token}")


def get_current_user(kappa_data: KappaDataApi = Depends(get_auth_kappa_data)) -> User:
    response = kappa_data.get_me().body
    yield User.parse_obj({
        "user_id": response["user_id"],
        "login": response["login"],
        "token": response["token"],
    })


@app.post("/signup/")
def signup(user: LoginUser, kappa_data: KappaDataApi = Depends(get_kappa_data)):
    from kappa_data_client.model.login_user import LoginUser
    return kappa_data.signup(LoginUser(username=user.username, password=user.password)).body


@app.post("/login/")
def login(user: LoginUser, kappa_data: KappaDataApi = Depends(get_kappa_data)):
    from kappa_data_client.model.login_user import LoginUser
    try:
        return kappa_data.login(LoginUser(username=user.username, password=user.password)).body
    except kappa_data_client.ApiException as response:
        raise HTTPException(status_code=response.status, detail=response.body)


class CreateFunction(BaseModel):
    name: str
    code: str


class GitHubResponse(BaseModel):
    text: str
    repos: list[str]


class CreatedFunction(BaseModel):
    fn_name: str
    created: bool
    related: GitHubResponse


@app.post("/functions/", response_model=CreatedFunction, responses={
    status.HTTP_406_NOT_ACCEPTABLE: {
        "description": "Code not acceptable"
    }
})
def create_function(create_fn: CreateFunction, user: User = Depends(get_current_user),
                    kappa_data: KappaDataApi = Depends(get_auth_kappa_data),
                    kappa_code: KappaCodeApi = Depends(get_kappa_code),
                    kappa_runner: KappaRunnerApi = Depends(get_kappa_runner)):
    code_id = str(uuid.uuid4())
    kappa_code.create_code(
        path_params={
            "code_id": code_id,
        },
        body=create_fn.code,
    )
    delete_code = lambda: kappa_code.delete_code(path_params={"code_id": code_id})
    try:
        fn = kappa_data.create_function(DataCreateFunction(
            name=create_fn.name,
            code_id=code_id,
        )).body
    except kappa_data_client.ApiException as e:
        delete_code()
        if e.status == 409:
            raise HTTPException(status.HTTP_409_CONFLICT)
        raise e
    try:
        kappa_runner.load_function(FunctionToLoad(fn_id=fn["fn_id"], code_id=code_id))
    except kappa_runner_client.ApiException as e:
        delete_code()
        kappa_data.delete_function(path_params={"fn_name": create_fn.name})
        if e.status == status.HTTP_406_NOT_ACCEPTABLE:
            raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, detail=json.loads(e.body)["detail"])
        raise e
    while not kappa_runner.is_function_loaded(path_params={"fn_id": fn["fn_id"]}).body["loaded"]:
        time.sleep(0.01)
    gh = requests.get(f"https://api.github.com/search/repositories?q={fn['name']}", headers={
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": config.github.api_version,
    }).json()
    return CreatedFunction(
        fn_name=create_fn.name,
        created=True,
        related=GitHubResponse(
            text=config.github.text,
            repos=list(map(lambda _: _["html_url"], gh["items"]))[:3],
        )
    )


@app.get("/functions/{fn_name}")
def execute_function(fn_name: str, request: Request, user: User = Depends(get_current_user),
                     kappa_data: KappaDataApi = Depends(get_kappa_data),
                     kappa_runner: KappaRunnerApi = Depends(get_kappa_runner)):
    fn = kappa_data.get_function(path_params={"fn_name": fn_name}).body
    return kappa_runner.execute_function(path_params={"fn_id": fn.fn_id},
                                         query_params=request.query_params)


@app.delete("/functions/{fn_name}")
def delete_function(fn_name: str, user: User = Depends(get_current_user),
                    kappa_data: KappaDataApi = Depends(get_kappa_data),
                    kappa_code: KappaCodeApi = Depends(get_kappa_code),
                    kappa_runner: KappaRunnerApi = Depends(get_kappa_runner)):
    fn = kappa_data.get_function(path_params={"fn_name": fn_name}).body
    kappa_code.delete_code(path_params={
        "code_id": fn.code_id,
    })
    kappa_data.delete_function(path_params={
        "fn_name": fn.name,
    })
    kappa_runner.unload_function(fn.fn_id)
    while kappa_runner.is_function_loaded(fn.fn_id).body.loaded:
        time.sleep(0.01)
