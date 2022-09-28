from itertools import chain, count
from functools import reduce
from typing import Iterator
from types import CodeType

from more_itertools import unique_everseen

from .instruction import HephaestusInstruction


def stack_size(instructions: list[HephaestusInstruction]) -> int:
    return reduce(
        lambda acc, instr: max(acc, acc + instr.get_stack_effect()),
        instructions,
        0,
    )


def merge_co_const(co_consts_a: tuple, co_consts_b: tuple) -> tuple[tuple, dict]:
    inject_const_map = {}
    value_index_map = {
        consts: index
        for index, consts in enumerate(co_consts_a)
    }

    for index, const in enumerate(co_consts_b):
        original_index = value_index_map.get(const, -1)
        if original_index != -1:
            inject_const_map[index] = original_index
            continue

        value_index_map[const] = len(value_index_map) - 1
        inject_const_map[index] = len(value_index_map) - 1

    return tuple(value_index_map.keys()), inject_const_map


def merge_co_name(co_names_a: tuple, co_names_b: tuple) -> tuple:
    return tuple(unique_everseen(chain(co_names_a, co_names_b)))


def to_bytes(instructions: list[HephaestusInstruction]) -> bytes:
    return b''.join([
        instruction.to_bytes()
        for instruction in instructions
    ])


def recalculate_offsets(
        instructions: list[HephaestusInstruction],
) -> Iterator[HephaestusInstruction]:
    offset = count(0, 2)
    for instruction in instructions:
        instruction.offset = next(offset)

        yield instruction


def create_code_object(
        origin: CodeType,
        stack_size: int,
        bytecode: bytes,
        consts: tuple,
        names: tuple,
        lnotab: bytes,
) -> CodeType:
    return CodeType(
        origin.co_argcount,
        origin.co_posonlyargcount,
        origin.co_kwonlyargcount,
        origin.co_nlocals,
        stack_size,
        origin.co_flags,
        bytecode,
        consts,
        names,
        origin.co_varnames,
        origin.co_filename,
        origin.co_name,
        origin.co_firstlineno,
        lnotab,
        origin.co_freevars,
        origin.co_cellvars,
    )


class LineAddressTable:
    pass


def calc_lnotab(code, listing) -> bytes:
    """
    String encoding the mapping from bytecode offsets to line numbers.
    https://github.com/python/cpython/blob/main/Objects/lnotab_notes.txt
    https://github.com/google/atheris/blob/master/src/version_dependent.py#L155
    """
    lnotab = []
    current_lineno = listing[0].lineno
    i = 0

    assert listing[0].lineno >= code.co_firstlineno

    if listing[0].lineno > code.co_firstlineno:
        delta_lineno = listing[0].lineno - code.co_firstlineno

        while delta_lineno > 127:
            lnotab.extend([0, 127])
            delta_lineno -= 127

        lnotab.extend([0, delta_lineno])

    while True:
        delta_bc = 0

        while i < len(listing) and listing[i].lineno == current_lineno:
            delta_bc += listing[i].get_size()
            i += 1

        if i >= len(listing):
            break

        assert delta_bc > 0

        delta_lineno = listing[i].lineno - current_lineno

        while delta_bc > 255:
            lnotab.extend([255, 0])
            delta_bc -= 255

        if delta_lineno < 0:
            while delta_lineno < -128:
                lnotab.extend([delta_bc, 0x80])
                delta_bc = 0
                delta_lineno += 128

            delta_lineno %= 256
        else:
            while delta_lineno > 127:
                lnotab.extend([delta_bc, 127])
                delta_bc = 0
                delta_lineno -= 127

        lnotab.extend([delta_bc, delta_lineno])
        current_lineno = listing[i].lineno

    return bytes(lnotab)
