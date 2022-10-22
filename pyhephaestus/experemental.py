import dis
from opcode import opmap
from typing import Callable


class Compare:
    pass


class Path:
    pass


class Const:
    pass


class Global:
    pass


class Assembler:
    ...


class Local(Assembler):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f'Local({self.name})'

    def __call__(self, *args, **kwargs):
        return [
            dis.Instruction(opname='LOAD_FAST', opcode=opmap['LOAD_FAST'], arg=0, argval=self.name, argrepr=self.name, offset=0, starts_line=None, is_jump_target=False),
        ]


class Call(Assembler):
    def __init__(self, callable_: Callable, *args, **kwargs):
        self._callable = callable_

    def __call__(self, *args, **kwargs):
        return [
            *self._callable(),
            dis.Instruction(opname='CALL_FUNCTION', opcode=opmap['CALL_FUNCTION'], arg=0, argval=0, argrepr='', offset=0, starts_line=None, is_jump_target=False),
            dis.Instruction(opname='POP_TOP', opcode=opmap['POP_TOP'], arg=None, argval=None, argrepr='', offset=0, starts_line=None, is_jump_target=False),
        ]


class Deref:
    pass


class LocalAssign:
    pass
