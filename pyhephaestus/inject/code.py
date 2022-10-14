import dis
from opcode import opmap
from types import CodeType


class Code:
    def __init__(self, origin: CodeType):
        self._origin = origin
        self._code = self._prepare()
        self._globals = {}
        self._locals = {}
        self._target = {}

    @property
    def code(self):
        return self._code

    def _prepare(self):
        return self._origin

    def _calculate_start_line(self):
        return 0

    def _load_const_code(self) -> dis.Instruction:
        return dis.Instruction(
                opname='LOAD_CONST',
                opcode=opmap['LOAD_CONST'],
                arg=1,
                argval=self._origin,
                argrepr=str(self._origin),
                offset=0,
                starts_line=self._calculate_start_line(),
                is_jump_target=False,
            )

    def _load_const_local_name(self, target: str) -> dis.Instruction:
        return dis.Instruction(
            opname='LOAD_CONST',
            opcode=opmap['LOAD_CONST'],
            arg=2,
            argval=f"'{target}.<locals>.{self._origin.co_name}'",
            argrepr=f"\"'{target}.<locals>.{self._origin.co_name}'\"",
            offset=2,
            starts_line=None,
            is_jump_target=False,
        )

    def _make_function(self) -> dis.Instruction:
        return dis.Instruction(
            opname='MAKE_FUNCTION',
            opcode=opmap['MAKE_FUNCTION'],
            arg=0,
            argval=0,
            argrepr='',
            offset=4,
            starts_line=None,
            is_jump_target=False,
        )

    def _store_fast(self) -> dis.Instruction:
        return dis.Instruction(
            opname='STORE_FAST',
            opcode=opmap['STORE_FAST'],
            arg=0,
            argval=f"'{self._origin.co_name}'",
            argrepr=f"'{self._origin.co_name}'",
            offset=6,
            starts_line=None,
            is_jump_target=False,
        )

    def instructions(self, target: str) -> list[dis.Instruction]:
        return [
            self._load_const_code(),
            self._load_const_local_name(target),
            self._make_function(),
            self._store_fast(),
        ]

    @property
    def co_argcount(self) -> int:
        return 0

    @property
    def co_names(self) -> tuple:
        return tuple()

    def co_consts(self, target: str) -> tuple[None, CodeType, str]:
        return None, self._origin, f'{target}.<locals>.{self._origin.co_name}'

    @property
    def co_nlocals(self):
        return 1

    @property
    def co_varnames(self) -> tuple[str]:
        return self._origin.co_name,

    def make_const(self, target):
        return {
            # 'co_argcount': '',
            # 'co_cellvars': '',
            'co_consts': (None, self._origin, f'{target}.<locals>.{self._origin.co_name}',),
            # 'co_filename': '',
            # 'co_firstlineno': '',
            # 'co_flags': '',
            # 'co_freevars': '',
            # 'co_lnotab': '',
            # 'co_name': '',
            # 'co_names': (),
            # 'co_nlocals': '',
            # 'co_stacksize': '',
            'co_varnames': (self._origin.co_name,),
        }
