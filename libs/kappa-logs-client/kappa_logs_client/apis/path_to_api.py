import typing_extensions

from kappa_logs_client.paths import PathValues
from kappa_logs_client.apis.paths.functions_fn_id_ import FunctionsFnId
from kappa_logs_client.apis.paths.functions_exec_exec_id_logs_ import FunctionsExecExecIdLogs

PathToApi = typing_extensions.TypedDict(
    'PathToApi',
    {
        PathValues.FUNCTIONS_FN_ID_: FunctionsFnId,
        PathValues.FUNCTIONS_EXEC_EXEC_ID_LOGS_: FunctionsExecExecIdLogs,
    }
)

path_to_api = PathToApi(
    {
        PathValues.FUNCTIONS_FN_ID_: FunctionsFnId,
        PathValues.FUNCTIONS_EXEC_EXEC_ID_LOGS_: FunctionsExecExecIdLogs,
    }
)
