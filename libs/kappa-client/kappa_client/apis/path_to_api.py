import typing_extensions

from kappa_client.paths import PathValues
from kappa_client.apis.paths.signup_ import Signup
from kappa_client.apis.paths.login_ import Login
from kappa_client.apis.paths.functions_ import Functions
from kappa_client.apis.paths.functions_fn_name import FunctionsFnName

PathToApi = typing_extensions.TypedDict(
    'PathToApi',
    {
        PathValues.SIGNUP_: Signup,
        PathValues.LOGIN_: Login,
        PathValues.FUNCTIONS_: Functions,
        PathValues.FUNCTIONS_FN_NAME: FunctionsFnName,
    }
)

path_to_api = PathToApi(
    {
        PathValues.SIGNUP_: Signup,
        PathValues.LOGIN_: Login,
        PathValues.FUNCTIONS_: Functions,
        PathValues.FUNCTIONS_FN_NAME: FunctionsFnName,
    }
)
