import uuid

from fastapi import Depends, FastAPI, HTTPException, Request
from pydantic import BaseModel
from starlette import status

import kappa_data_client
import kappa_data_client.apis.tags.default_api
import kappa_fn_code_client
import kappa_fn_code_client.apis.tags.default_api
import kappa_fn_logs_client
import kappa_fn_logs_client.apis.tags.default_api
from kappa_fn_logs_client.model.create_log import CreateLog
from kappa_runner import runner
from kappa_runner.config import config


app = FastAPI(
    title="kappa-runner",
    version="0.0.0",
    author="dpdani",
    generate_unique_id_function=lambda route: f"{route.name}",
)

KappaDataApi = kappa_data_client.apis.tags.default_api.DefaultApi
KappaCodeApi = kappa_fn_code_client.apis.tags.default_api.DefaultApi
KappaFnLogsApi = kappa_fn_logs_client.apis.tags.default_api.DefaultApi


def get_kappa_data() -> KappaDataApi:
    conf = kappa_data_client.Configuration(config.kappa.data)
    with kappa_data_client.ApiClient(conf) as api_client:
        kappa_data = KappaDataApi(api_client)
        yield kappa_data


def get_kappa_code() -> KappaCodeApi:
    conf = kappa_fn_code_client.Configuration(config.kappa.fn_code)
    with kappa_fn_code_client.ApiClient(conf) as api_client:
        kappa_code = KappaCodeApi(api_client)
        yield kappa_code


def get_kappa_fn_logs() -> KappaFnLogsApi:
    conf = kappa_fn_code_client.Configuration(config.kappa.fn_logs)
    with kappa_fn_logs_client.ApiClient(conf) as api_client:
        kappa_code = KappaFnLogsApi(api_client)
        yield kappa_code


class FunctionToLoad(BaseModel):
    fn_id: int
    code_id: str


@app.post("/functions/load", responses={
    status.HTTP_406_NOT_ACCEPTABLE: {
        "description": "Code not acceptable",
    }
})
def load_function(fn: FunctionToLoad, kappa_data: KappaDataApi = Depends(get_kappa_data),
                  kappa_code: KappaCodeApi = Depends(get_kappa_code)):
    fn = kappa_data.get_function_by_id(path_params={"fn_id": fn.fn_id}).body
    code = kappa_code.get_code(path_params={"code_id": fn["code_id"]}).body.as_str_oapg
    try:
        runner.load_function(fn["fn_id"], code)
    except runner.InvalidCode:
        raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE,
                            detail="Invalid code.")
    except runner.NoMainException:
        raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE,
                            detail="Function 'main()' not found inside code.")


class LoadedFunction(BaseModel):
    loaded: bool


@app.get("/functions/{fn_id}/isLoaded", response_model=LoadedFunction)
def is_function_loaded(fn_id: int):
    return LoadedFunction(loaded=fn_id in runner.loaded_functions)


class Execution(BaseModel):
    fn_id: int
    exec_id: str
    status: str
    output: dict


@app.get("/functions/{fn_id}/", response_model=Execution, openapi_extra={
    "parameters": [  # specify presence of arbitrary query parameters
        {
            "in": "query",
            "name": "params",
            "schema": {
                "type": "object",
                "additionalProperties": {
                    "type": "string",
                }
            },
            "style": "form",
            "explode": True,
        }
    ]
})
def execute_function(fn_id: int, request: Request, kappa_data: KappaDataApi = Depends(get_kappa_data),
                     kappa_fn_logs: KappaFnLogsApi = Depends(get_kappa_fn_logs)):
    if fn_id not in runner.loaded_functions:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    exec_id = str(uuid.uuid4())
    kappa_data.log_function_execution(path_params={
        "fn_id": fn_id,
        "exec_id": exec_id,
    })
    try:
        run = runner.execute_function(fn_id, arguments=dict(request.query_params))
    except runner.InvalidArgument as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail={
            "invalid_argument": e.arg,
        })
    kappa_fn_logs.create_log(CreateLog(
        fn=fn_id,
        exec_id=exec_id,
        stdout=run.capture.stdout.getvalue(),
        stderr=run.capture.stderr.getvalue(),
    ))
    return Execution(
        fn_id=fn_id,
        exec_id=exec_id,
        status="executed",
        output=run.output if run.output is not None else dict(),
    )


@app.delete("/functions/{fn_id}/")
def unload_function(fn_id: int):
    try:
        runner.unload_function(fn_id)
    except runner.FunctionNotLoaded:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
