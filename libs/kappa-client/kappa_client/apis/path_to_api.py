import typing_extensions

from kappa_client.paths import PathValues
from kappa_client.apis.paths.signup_ import Signup
from kappa_client.apis.paths.login_ import Login
from kappa_client.apis.paths.user_me import UserMe
from kappa_client.apis.paths.functions_ import Functions
from kappa_client.apis.paths.functions_fn_name import FunctionsFnName
from kappa_client.apis.paths.functions_fn_name_logs_ import FunctionsFnNameLogs

PathToApi = typing_extensions.TypedDict(
    'PathToApi',
    {
        PathValues.SIGNUP_: Signup,
        PathValues.LOGIN_: Login,
        PathValues.USER_ME: UserMe,
        PathValues.FUNCTIONS_: Functions,
        PathValues.FUNCTIONS_FN_NAME: FunctionsFnName,
        PathValues.FUNCTIONS_FN_NAME_LOGS_: FunctionsFnNameLogs,
    }
)

path_to_api = PathToApi(
    {
        PathValues.SIGNUP_: Signup,
        PathValues.LOGIN_: Login,
        PathValues.USER_ME: UserMe,
        PathValues.FUNCTIONS_: Functions,
        PathValues.FUNCTIONS_FN_NAME: FunctionsFnName,
        PathValues.FUNCTIONS_FN_NAME_LOGS_: FunctionsFnNameLogs,
    }
)
