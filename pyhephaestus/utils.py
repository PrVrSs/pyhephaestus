import hashlib
import marshal
from types import CodeType


def str_to_code(code: str) -> CodeType:
    return compile(code, '<string>', mode='exec')


def code_hash(code: CodeType) -> str:
    return hashlib.sha1(marshal.dumps(code)).hexdigest()
