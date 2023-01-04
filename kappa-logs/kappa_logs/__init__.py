import json
import datetime

from fastapi import Depends, FastAPI
from pydantic import BaseModel

import kappa_data_client
import kappa_data_client.apis.tags.default_api
import kappa_fn_logs_client
import kappa_fn_logs_client.apis.tags.default_api
from kappa_logs.config import config


app = FastAPI(
    title="kappa-logs",
    version="0.0.0",
    author="dpdani",
    generate_unique_id_function=lambda route: f"{route.name}",
)

KappaDataApi = kappa_data_client.apis.tags.default_api.DefaultApi
KappaFnLogsApi = kappa_fn_logs_client.apis.tags.default_api.DefaultApi


def get_kappa_data() -> KappaDataApi:
    conf = kappa_data_client.Configuration(config.kappa.data)
    with kappa_data_client.ApiClient(conf) as api_client:
        kappa_data = KappaDataApi(api_client)
        yield kappa_data


def get_kappa_fn_logs() -> KappaFnLogsApi:
    conf = kappa_fn_logs_client.Configuration(config.kappa.fn_logs)
    with kappa_fn_logs_client.ApiClient(conf) as api_client:
        kappa_data = KappaFnLogsApi(api_client)
        yield kappa_data


class Log(BaseModel):
    ts: datetime.datetime
    content: str


class Logs(BaseModel):
    logs: list[Log]


def process_fn_logs(fn_logs) -> list[Log]:
    fn_logs: list[Log] = list(map(
        lambda _: Log(
            ts=_["ts"],
            content=json.dumps({
                "exec_id": _["exec_id"],
                "stdout": _["stdout"],
                "stderr": _["stderr"],
            }),
        ),
        fn_logs
    ))
    for log in fn_logs:
        log.ts = log.ts.replace(tzinfo=datetime.timezone.utc, hour=log.ts.hour + 1)
    return fn_logs


@app.get("/functions/{fn_id}/", response_model=Logs)
def get_fn_logs(fn_id: int, kappa_data: KappaDataApi = Depends(get_kappa_data),
                kappa_fn_logs: KappaFnLogsApi = Depends(get_kappa_fn_logs)) -> Logs:
    data_logs: list[Log] = list(map(
        lambda _: Log(
            ts=_["time"],
            content=_["content"],
        ),
        kappa_data.get_function_logs(path_params={"fn_id": fn_id}).body
    ))
    print(data_logs)
    fn_logs = process_fn_logs(kappa_fn_logs.get_logs(path_params={"fn": fn_id}).body["logs"])
    print(fn_logs)
    logs = [
        *data_logs,
        *fn_logs,
    ]
    return Logs(logs=sorted(logs, key=lambda _: _.ts))


@app.get("/functions/exec/{exec_id}/logs/", response_model=Logs)
def get_exec_logs(exec_id: str, kappa_fn_logs: KappaFnLogsApi = Depends(get_kappa_fn_logs)):
    logs = process_fn_logs(
        kappa_fn_logs.get_exec_logs(path_params={"exec_id": exec_id}).body["logs"]
    )
    return Logs(logs=sorted(logs, key=lambda _: _.ts))
