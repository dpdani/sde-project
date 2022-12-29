import io
import sys
from contextlib import contextmanager
from dataclasses import dataclass
from types import ModuleType


loaded_functions: dict[int, ModuleType] = dict()  # fn_id -> code


class NoMainException(Exception):
    pass


class FunctionNotLoaded(Exception):
    pass


class FunctionLoaded(Exception):
    pass


def load_function(fn_id: int, code: str):
    if fn_id in loaded_functions:
        raise FunctionLoaded
    mod = ModuleType(f'fn_{fn_id}')
    exec(code, mod.__dict__)
    if not hasattr(mod, "main"):
        raise NoMainException
    if not callable(mod.main):
        raise NoMainException
    loaded_functions[fn_id] = mod


def unload_function(fn_id: int):
    if fn_id not in loaded_functions:
        raise FunctionNotLoaded
    del loaded_functions[fn_id]


@dataclass
class Capture:
    stdout: io.StringIO
    stderr: io.StringIO


@dataclass
class RunnerExecution:
    output: dict
    capture: Capture


@contextmanager
def capture():
    real_stdout, real_stderr = sys.stdout, sys.stderr
    capt = Capture(io.StringIO(), io.StringIO())
    sys.stdout, sys.stderr = capt.stdout, capt.stderr
    yield capt
    sys.stdout, sys.stderr = real_stdout, real_stderr


def execute_function(fn_id: int, arguments: dict) -> RunnerExecution:
    if fn_id not in loaded_functions:
        raise FunctionNotLoaded
    with capture() as capt:
        output = loaded_functions[fn_id].main(**arguments)
        return RunnerExecution(
            output=output,
            capture=capt,
        )
