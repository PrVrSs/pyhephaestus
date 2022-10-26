__all__ = 'CONDITIONAL_JUMPS', 'UNCONDITIONAL_JUMPS', 'HAVE_REL_REFERENCE', 'HAVE_ABS_REFERENCE'


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
