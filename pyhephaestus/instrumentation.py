from .merger import merge, Location
from .utils import str_to_code


class MetaInstrumentator(type):
    def __new__(mcs, name, bases, dct):
        if not bases:
            return super().__new__(mcs, name, bases, dct)

        code = dct['target']

        if dct['on_enter'] is not None:
            code = merge(
                original=code,
                injected=str_to_code(dct['on_enter']),
                location=Location.START,
            )

        if dct['on_exit'] is not None:
            code = merge(
                original=code,
                injected=str_to_code(dct['on_exit']),
                location=Location.END,
            )

        return code


class FuncInstrumentator(metaclass=MetaInstrumentator):
    target = None
    on_enter = None
    on_exit = None


class instrumentation_wraps:
    def __init__(self, on_enter: str | None = None, on_exit: str | None = None):
        self._on_enter = on_enter
        self._on_exit = on_exit

    def __call__(self, func):
        if not callable(func):
            raise TypeError('the argument must be callable')

        code = func.__code__
        if self._on_enter is not None:
            code = merge(
                original=code,
                injected=str_to_code(self._on_enter),
                location=Location.START,
            )

        if self._on_exit is not None:
            code = merge(
                original=code,
                injected=str_to_code(self._on_exit),
                location=Location.END,
            )

        func.__code__ = code

        return func
