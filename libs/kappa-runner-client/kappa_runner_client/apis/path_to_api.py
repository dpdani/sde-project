import typing_extensions

from kappa_runner_client.paths import PathValues
from kappa_runner_client.apis.paths.functions_load import FunctionsLoad
from kappa_runner_client.apis.paths.functions_fn_id_is_loaded import FunctionsFnIdIsLoaded
from kappa_runner_client.apis.paths.functions_fn_id_ import FunctionsFnId

PathToApi = typing_extensions.TypedDict(
    'PathToApi',
    {
        PathValues.FUNCTIONS_LOAD: FunctionsLoad,
        PathValues.FUNCTIONS_FN_ID_IS_LOADED: FunctionsFnIdIsLoaded,
        PathValues.FUNCTIONS_FN_ID_: FunctionsFnId,
    }
)

path_to_api = PathToApi(
    {
        PathValues.FUNCTIONS_LOAD: FunctionsLoad,
        PathValues.FUNCTIONS_FN_ID_IS_LOADED: FunctionsFnIdIsLoaded,
        PathValues.FUNCTIONS_FN_ID_: FunctionsFnId,
    }
)
