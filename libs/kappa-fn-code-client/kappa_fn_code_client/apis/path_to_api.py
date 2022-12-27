import typing_extensions

from kappa_fn_code_client.paths import PathValues
from kappa_fn_code_client.apis.paths.code_code_id_ import CodeCodeId

PathToApi = typing_extensions.TypedDict(
    'PathToApi',
    {
        PathValues.CODE_CODE_ID_: CodeCodeId,
    }
)

path_to_api = PathToApi(
    {
        PathValues.CODE_CODE_ID_: CodeCodeId,
    }
)
