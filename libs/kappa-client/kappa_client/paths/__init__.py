# do not import all endpoints into this module because that uses a lot of memory and stack frames
# if you need the ability to import all endpoints from this module, import them with
# from kappa_client.apis.path_to_api import path_to_api

import enum


class PathValues(str, enum.Enum):
    SIGNUP_ = "/signup/"
    LOGIN_ = "/login/"
    USER_ME = "/user/me"
    FUNCTIONS_ = "/functions/"
    FUNCTIONS_FN_NAME = "/functions/{fn_name}"
    FUNCTIONS_FN_NAME_LOGS_ = "/functions/{fn_name}/logs/"
    FUNCTIONS_EXEC_EXEC_ID_LOGS_ = "/functions/exec/{exec_id}/logs/"
    BILL_ = "/bill/"
