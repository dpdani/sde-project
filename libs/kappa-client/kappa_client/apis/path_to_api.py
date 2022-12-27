import typing_extensions

from kappa_client.paths import PathValues
from kappa_client.apis.paths.login_ import Login
from kappa_client.apis.paths.users_me_ import UsersMe
from kappa_client.apis.paths.functions_ import Functions
from kappa_client.apis.paths.functions_fn_name_ import FunctionsFnName

PathToApi = typing_extensions.TypedDict(
    'PathToApi',
    {
        PathValues.LOGIN_: Login,
        PathValues.USERS_ME_: UsersMe,
        PathValues.FUNCTIONS_: Functions,
        PathValues.FUNCTIONS_FN_NAME_: FunctionsFnName,
    }
)

path_to_api = PathToApi(
    {
        PathValues.LOGIN_: Login,
        PathValues.USERS_ME_: UsersMe,
        PathValues.FUNCTIONS_: Functions,
        PathValues.FUNCTIONS_FN_NAME_: FunctionsFnName,
    }
)
