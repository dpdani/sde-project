# do not import all endpoints into this module because that uses a lot of memory and stack frames
# if you need the ability to import all endpoints from this module, import them with
# from kappa_fn_logs_client.paths.logs_fn_ import Api

from kappa_fn_logs_client.paths import PathValues

path = PathValues.LOGS_FN_