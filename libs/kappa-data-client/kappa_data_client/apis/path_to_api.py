import typing_extensions

from kappa_data_client.paths import PathValues
from kappa_data_client.apis.paths.login_ import Login
from kappa_data_client.apis.paths.signup_ import Signup
from kappa_data_client.apis.paths.users_me_ import UsersMe
from kappa_data_client.apis.paths.functions_ import Functions
from kappa_data_client.apis.paths.functions_fn_name_ import FunctionsFnName
from kappa_data_client.apis.paths.functions_id_fn_id_ import FunctionsIdFnId
from kappa_data_client.apis.paths.functions_fn_id_logs_ import FunctionsFnIdLogs
from kappa_data_client.apis.paths.functions_fn_id_logs_execution_exec_id import FunctionsFnIdLogsExecutionExecId
from kappa_data_client.apis.paths.bill_ import Bill

PathToApi = typing_extensions.TypedDict(
    'PathToApi',
    {
        PathValues.LOGIN_: Login,
        PathValues.SIGNUP_: Signup,
        PathValues.USERS_ME_: UsersMe,
        PathValues.FUNCTIONS_: Functions,
        PathValues.FUNCTIONS_FN_NAME_: FunctionsFnName,
        PathValues.FUNCTIONS_ID_FN_ID_: FunctionsIdFnId,
        PathValues.FUNCTIONS_FN_ID_LOGS_: FunctionsFnIdLogs,
        PathValues.FUNCTIONS_FN_ID_LOGS_EXECUTION_EXEC_ID: FunctionsFnIdLogsExecutionExecId,
        PathValues.BILL_: Bill,
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
        PathValues.FUNCTIONS_FN_ID_LOGS_: FunctionsFnIdLogs,
        PathValues.FUNCTIONS_FN_ID_LOGS_EXECUTION_EXEC_ID: FunctionsFnIdLogsExecutionExecId,
        PathValues.BILL_: Bill,
    }
)
