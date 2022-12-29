import typing_extensions

from kappa_client.paths import PathValues
from kappa_client.apis.paths.login_ import Login
from kappa_client.apis.paths.signup_ import Signup
from kappa_client.apis.paths.users_me_ import UsersMe
from kappa_client.apis.paths.functions_ import Functions
from kappa_client.apis.paths.functions_fn_name_ import FunctionsFnName
from kappa_client.apis.paths.functions_id_fn_id_ import FunctionsIdFnId
from kappa_client.apis.paths.functions_fn_name_logs_ import FunctionsFnNameLogs
from kappa_client.apis.paths.functions_fn_id_logs_execution_exec_id import FunctionsFnIdLogsExecutionExecId

PathToApi = typing_extensions.TypedDict(
    'PathToApi',
    {
        PathValues.LOGIN_: Login,
        PathValues.SIGNUP_: Signup,
        PathValues.USERS_ME_: UsersMe,
        PathValues.FUNCTIONS_: Functions,
        PathValues.FUNCTIONS_FN_NAME_: FunctionsFnName,
        PathValues.FUNCTIONS_ID_FN_ID_: FunctionsIdFnId,
        PathValues.FUNCTIONS_FN_NAME_LOGS_: FunctionsFnNameLogs,
        PathValues.FUNCTIONS_FN_ID_LOGS_EXECUTION_EXEC_ID: FunctionsFnIdLogsExecutionExecId,
    }
)

path_to_api = PathToApi(
    {
        PathValues.LOGIN_: Login,
        PathValues.SIGNUP_: Signup,
        PathValues.USERS_ME_: UsersMe,
        PathValues.FUNCTIONS_: Functions,
        PathValues.FUNCTIONS_FN_NAME_: FunctionsFnName,
        PathValues.FUNCTIONS_ID_FN_ID_: FunctionsIdFnId,
        PathValues.FUNCTIONS_FN_NAME_LOGS_: FunctionsFnNameLogs,
        PathValues.FUNCTIONS_FN_ID_LOGS_EXECUTION_EXEC_ID: FunctionsFnIdLogsExecutionExecId,
    }
)
