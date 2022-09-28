import sys


def _pyc_header(version: tuple[int, int]) -> int:
    if version >= (3, 10):
        return 16

    return 12


PYTHON_VERSION: tuple[int, int] = sys.version_info[:2]
PYC_HEADER = _pyc_header(PYTHON_VERSION)

CO_FIELDS = frozenset((
    'co_argcount',
    'co_cellvars',
    'co_consts',
    'co_filename',
    'co_firstlineno',
    'co_flags',
    'co_freevars',
    'co_lnotab',
    'co_name',
    'co_names',
    'co_nlocals',
    'co_stacksize',
    'co_varnames',
))

MERGE_BLACKLIST = frozenset((
    'co_code',
    'co_firstlineno',
    'co_name',
    'co_filename',
    'co_lnotab',
    'co_flags',
    'co_argcount',
))

CONDITIONAL_JUMPS = [
    'FOR_ITER',
    'JUMP_IF_FALSE_OR_POP',
    'JUMP_IF_TRUE_OR_POP',
    'JUMP_IF_NOT_EXC_MATCH',
    'POP_JUMP_IF_FALSE',
    'POP_JUMP_IF_TRUE',
]

UNCONDITIONAL_JUMPS = [
    'JUMP_FORWARD',
    'JUMP_ABSOLUTE',
    'CONTINUE_LOOP',
    'CALL_FINALLY',
]

HAVE_REL_REFERENCE = [
    'CALL_FINALLY',
    'JUMP_FORWARD',
    'FOR_ITER',
    'SETUP_WITH',
    'SETUP_FINALLY',
    'SETUP_LOOP',
    'SETUP_EXCEPT',
]

HAVE_ABS_REFERENCE = [
    'CONTINUE_LOOP',
    'JUMP_IF_TRUE_OR_POP',
    'JUMP_IF_FALSE_OR_POP',
    'JUMP_ABSOLUTE',
    'JUMP_IF_NOT_EXC_MATCH',
    'POP_JUMP_IF_FALSE',
    'POP_JUMP_IF_TRUE',
]

LOAD_BUILD_CLASS = 'LOAD_BUILD_CLASS'
MAKE_FUNCTION = 'MAKE_FUNCTION'


__all__ = (
    'PYTHON_VERSION',
    'PYC_HEADER',
    'CONDITIONAL_JUMPS',
    'UNCONDITIONAL_JUMPS',
    'HAVE_ABS_REFERENCE',
    'HAVE_REL_REFERENCE',
    'LOAD_BUILD_CLASS',
    'MAKE_FUNCTION',
)
