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
