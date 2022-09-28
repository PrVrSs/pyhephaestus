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
            *inserted[:-2],
            *origin,
        ]

    return [
        *origin[:-2],
        *inserted[:-2],
        *origin[-2:]
    ]


def make_instructions(code: CodeType) -> list[HephaestusInstruction]:
    return [
        HephaestusInstruction(instruction)
        for instruction in dis.get_instructions(code)
    ]


class Merger:
    def __init__(self, origin: CodeType, inject: CodeType, location: Location):
        self._co_origin = origin
        self._co_inject = inject

        self._consts, self.inject_origin_const_map = merge_co_const(
            self._co_origin.co_consts, self._co_inject.co_consts)

        self._origin_instructions = make_instructions(origin)
        self._inject_instructions = list(self._prepare_injected(make_instructions(inject)))

        self._merge_instructions = merge_instructions(
            origin=self._origin_instructions,
            inserted=self._inject_instructions,
            location=location,
        )

        recalculate_offsets(self._merge_instructions)

    def _prepare_injected(
            self,
            instructions: list[HephaestusInstruction],
    ) -> Iterator[HephaestusInstruction]:
        for instruction in instructions:
            if instruction.opname == 'LOAD_NAME' and instruction.argrepr in dir(builtins):
                instruction = HephaestusInstruction(
                    dis.Instruction(
                        opname='LOAD_GLOBAL',
                        opcode=116,
                        arg=instruction.arg,
                        argval=instruction.argval,
                        argrepr=instruction.argrepr,
                        offset=instruction.offset,
                        starts_line=instruction.starts_line,
                        is_jump_target=instruction.is_jump_target
                    )
                )

            if instruction.opname == 'LOAD_CONST':
                instruction.arg = self.inject_origin_const_map[instruction.arg]

            instruction.lineno = self._co_origin.co_firstlineno

            yield instruction

    def merge(self) -> CodeType:
        return create_code_object(
            origin=self._co_origin,
            stack_size=stack_size(self._merge_instructions),
            bytecode=to_bytes(self._merge_instructions),
            consts=self._consts,
            names=merge_co_name(self._co_origin.co_names, self._co_inject.co_names),
            lnotab=calc_lnotab(self._co_origin, self._merge_instructions),
        )


def merge(original: CodeType, injected: CodeType, location: Location) -> CodeType:
    return Merger(original, injected, location).merge()
