# do not import all endpoints into this module because that uses a lot of memory and stack frames
# if you need the ability to import all endpoints from this module, import them with
# from kappa_client.apis.path_to_api import path_to_api

import enum


class PathValues(str, enum.Enum):
    LOGIN_ = "/login/"
    USERS_ME_ = "/users/me/"
    FUNCTIONS_ = "/functions/"
    FUNCTIONS_FN_NAME_ = "/functions/{fn_name}/"
