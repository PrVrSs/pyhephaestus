import dis


class HephaestusInstruction:

    opname = property(lambda self: self._instruction.opname)
    argval = property(lambda self: self._instruction.argval)
    argrepr = property(lambda self: self._instruction.argrepr)
    starts_line = property(lambda self: self._instruction.starts_line)
    is_jump_target = property(lambda self: self._instruction.is_jump_target)
    oparg = property(lambda self: self.arg if self.has_argument() else None)

    # offset = property(lambda self: self._instruction.offset)
    # opcode = property(lambda self: self._instruction.opcode)
    # arg = property(lambda self: self._instruction.arg or 0)
    # lineno = property(lambda self: self._instruction.starts_line or 0)

    def __init__(self, instruction: dis.Instruction, min_size: int = 0):
        self._instruction = instruction
        self._min_size = min_size
        self.offset = instruction.offset
        self.arg = instruction.arg or 0
        self.opcode = instruction.opcode
        self.mnemonic = dis.opname[instruction.opcode]
        self.lineno = instruction.starts_line or 0

    def __repr__(self):
        return (
            f'Instruction('
            f'opname={self.opname}, '
            f'opcode={self.opcode}, '
            f'arg={self.arg}, '
            f'argval={self.argval}, '
            f'argrepr={self.argrepr}, '
            f'offset={self.offset}, '
            f'starts_line={self.starts_line}, '
            f'is_jump_target={self.is_jump_target})'
        )

    def _get_arg_size(self) -> int:
        if self.arg >= (1 << 24):
            return 8
        elif self.arg >= (1 << 16):
            return 6
        elif self.arg >= (1 << 8):
            return 4

        return 2

    def get_size(self) -> int:
        return max(self._get_arg_size(), self._min_size)

    def get_stack_effect(self):
        return dis.stack_effect(self.opcode, self.oparg)

    def has_argument(self) -> bool:
        return self.opcode >= dis.HAVE_ARGUMENT

    def to_bytes(self) -> bytes:
        size = self._get_arg_size()
        arg = self.arg
        ret = [self.opcode, arg & 0xff]

        for _ in range(size // 2 - 1):
            arg >>= 8
            ret = [dis.opmap['EXTENDED_ARG'], arg & 0xff] + ret

        while len(ret) < self._min_size:
            ret = [dis.opmap['EXTENDED_ARG'], 0] + ret

        assert len(ret) == self.get_size()

        return bytes(ret)
