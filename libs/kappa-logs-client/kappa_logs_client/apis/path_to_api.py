import typing_extensions

from kappa_logs_client.paths import PathValues
from kappa_logs_client.apis.paths.functions_fn_id_ import FunctionsFnId

PathToApi = typing_extensions.TypedDict(
    'PathToApi',
    {
        PathValues.FUNCTIONS_FN_ID_: FunctionsFnId,
    }
)

path_to_api = PathToApi(
    {
        PathValues.FUNCTIONS_FN_ID_: FunctionsFnId,
    }
)
