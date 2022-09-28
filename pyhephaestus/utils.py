from types import CodeType


def str_to_code(code: str) -> CodeType:
    return compile(code, '<string>', mode='exec')
