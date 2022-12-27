# do not import all endpoints into this module because that uses a lot of memory and stack frames
# if you need the ability to import all endpoints from this module, import them with
# from kappa_client.paths.users_me_ import Api

from kappa_client.paths import PathValues

path = PathValues.USERS_ME_