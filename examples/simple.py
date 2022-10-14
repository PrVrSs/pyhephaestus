import dis
from opcode import opmap

from pyhephaestus import instrumentation_wraps


def insert_fn():
    print('inserted')


call_insert_fn = [
    dis.Instruction(opname='LOAD_FAST', opcode=opmap['LOAD_FAST'], arg=0, argval='insert_fn', argrepr='insert_fn', offset=0, starts_line=None, is_jump_target=False),
    dis.Instruction(opname='CALL_FUNCTION', opcode=opmap['CALL_FUNCTION'], arg=0, argval=0, argrepr='', offset=0, starts_line=None, is_jump_target=False),
    dis.Instruction(opname='POP_TOP', opcode=opmap['POP_TOP'], arg=None, argval=None, argrepr='', offset=0, starts_line=None, is_jump_target=False),
]


@instrumentation_wraps(
    on_enter=insert_fn.__code__,
    on_exit=call_insert_fn,
)
def some_function():
    print('Do work')


if __name__ == '__main__':
    some_function()
