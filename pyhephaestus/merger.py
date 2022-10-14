import builtins
import dis
from enum import IntFlag
from types import CodeType
from typing import Iterator

from .code_utils import (
    merge_co_const,
    merge_co_name,
    to_bytes,
    stack_size,
    recalculate_offsets,
    create_code_object,
    calc_lnotab,
)
from .instruction import HephaestusInstruction


class Location(IntFlag):
    START = 1
    END = 2


def merge_instructions(
        origin: list[HephaestusInstruction],
        inserted: list[HephaestusInstruction],
        location: Location,
) -> list[HephaestusInstruction]:
    if location is Location.START:
        return [
            *inserted,
            *origin,
        ]

    return [
        *origin[:-2],
        *inserted,
        *origin[-2:]
    ]


def make_instructions(code: CodeType) -> list[HephaestusInstruction]:
    return [
        HephaestusInstruction(instruction)
        for instruction in dis.get_instructions(code)
    ]


class Merger:
    def __init__(self, origin: CodeType, inject, location: Location):
        self._co_origin = origin
        self._co_inject = inject

        self._consts, self.inject_origin_const_map = merge_co_const(
            self._co_origin.co_consts, self._co_inject.co_consts(target=self._co_origin.co_name))

        self._origin_instructions = list(self._prepare_origin(make_instructions(origin)))
        self._inject_instructions = list(self._prepare_injected([HephaestusInstruction(instr) for instr in self._co_inject.instructions(self._co_origin.co_name)], location))

        self._merge_instructions = merge_instructions(
            origin=self._origin_instructions,
            inserted=self._inject_instructions,
            location=location,
        )

        self._merge_instructions = list(recalculate_offsets(self._merge_instructions))

    def _prepare_origin(self, instructions):
        for instr in instructions:
            # if instr.opname == 'LOAD_GLOBAL' and instr.argval not in dir(builtins):
            #     instr = HephaestusInstruction(
            #         dis.Instruction(
            #             opname='LOAD_FAST',
            #             opcode=124,
            #             arg=0,
            #             argval=instr.argval,
            #             argrepr=instr.argrepr,
            #             offset=instr.offset,
            #             starts_line=instr.starts_line,
            #             is_jump_target=instr.is_jump_target,
            #         )
            #     )

            yield instr

    def _prepare_injected(
            self,
            instructions: list[HephaestusInstruction],
            location,
    ) -> Iterator[HephaestusInstruction]:
        for instruction in instructions:
            if instruction.opname == 'LOAD_CONST':
                instruction.arg = self.inject_origin_const_map[instruction.arg]

            instruction.lineno = self._co_origin.co_firstlineno

            yield instruction

    def merge(self) -> CodeType:
        return create_code_object(
            co_argcount=merge_argcount(self._co_origin.co_argcount, self._co_inject.co_argcount),
            co_posonlyargcount=self._co_origin.co_posonlyargcount,
            co_kwonlyargcount=self._co_origin.co_kwonlyargcount,
            co_nlocals=self._co_origin.co_nlocals + self._co_inject.co_nlocals,
            # co_stacksize=stack_size(self._merge_instructions),
            co_stacksize=2,
            co_flags=self._co_origin.co_flags,
            # co_code=to_bytes(self._merge_instructions),
            co_code=b''.join([instr for instr in to_bytes(self._merge_instructions)]),
            co_consts=self._consts,
            co_names=merge_co_name(self._co_origin.co_names, self._co_inject.co_names),
            co_varnames=self._co_origin.co_varnames + self._co_inject.co_varnames,
            co_filename=self._co_origin.co_filename,
            co_name=self._co_origin.co_name,
            co_firstlineno=self._co_origin.co_firstlineno,
            co_lnotab=calc_lnotab(self._co_origin, self._merge_instructions),
            co_freevars=self._co_origin.co_freevars,
            co_cellvars=self._co_origin.co_cellvars,
        )


def merge_argcount(a, b):
    return a + b


def merge(original: CodeType, injected, location: Location) -> CodeType:
    return Merger(original, injected, location).merge()
