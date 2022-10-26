import sys


__all__ = ('PYTHON_VERSION', 'PYC_HEADER', 'CO_FIELDS', 'MERGE_BLACKLIST', 'LOAD_BUILD_CLASS',
           'MAKE_FUNCTION')


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


LOAD_BUILD_CLASS = 'LOAD_BUILD_CLASS'
MAKE_FUNCTION = 'MAKE_FUNCTION'
