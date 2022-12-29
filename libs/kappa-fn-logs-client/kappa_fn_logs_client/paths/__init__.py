# do not import all endpoints into this module because that uses a lot of memory and stack frames
# if you need the ability to import all endpoints from this module, import them with
# from kappa_fn_logs_client.apis.path_to_api import path_to_api

import enum


class PathValues(str, enum.Enum):
    LOGS_ = "/logs/"
    LOGS_FN_ = "/logs/{fn}/"
