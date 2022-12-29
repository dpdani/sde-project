import typing_extensions

from kappa_fn_logs_client.paths import PathValues
from kappa_fn_logs_client.apis.paths.logs_ import Logs
from kappa_fn_logs_client.apis.paths.logs_fn_ import LogsFn

PathToApi = typing_extensions.TypedDict(
    'PathToApi',
    {
        PathValues.LOGS_: Logs,
        PathValues.LOGS_FN_: LogsFn,
    }
)

path_to_api = PathToApi(
    {
        PathValues.LOGS_: Logs,
        PathValues.LOGS_FN_: LogsFn,
    }
)
