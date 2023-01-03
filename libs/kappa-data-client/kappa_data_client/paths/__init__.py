# do not import all endpoints into this module because that uses a lot of memory and stack frames
# if you need the ability to import all endpoints from this module, import them with
# from kappa_data_client.apis.path_to_api import path_to_api

import enum


class PathValues(str, enum.Enum):
    LOGIN_ = "/login/"
    SIGNUP_ = "/signup/"
    USERS_ME_ = "/users/me/"
    FUNCTIONS_ = "/functions/"
    FUNCTIONS_FN_NAME_ = "/functions/{fn_name}/"
    FUNCTIONS_ID_FN_ID_ = "/functions/id/{fn_id}/"
    FUNCTIONS_FN_ID_LOGS_ = "/functions/{fn_id}/logs/"
    FUNCTIONS_FN_ID_LOGS_EXECUTION_EXEC_ID = "/functions/{fn_id}/logs/execution/{exec_id}"
