# do not import all endpoints into this module because that uses a lot of memory and stack frames
# if you need the ability to import all endpoints from this module, import them with
# from kappa_runner_client.apis.path_to_api import path_to_api

import enum


class PathValues(str, enum.Enum):
    FUNCTIONS_LOAD = "/functions/load"
    FUNCTIONS_FN_ID_IS_LOADED = "/functions/{fn_id}/isLoaded"
    FUNCTIONS_FN_ID_ = "/functions/{fn_id}/"
