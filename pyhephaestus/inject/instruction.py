import dis


class Instruction:
    def __init__(self, origin: list[dis.Instruction]):
        self._origin = origin

    def instructions(self, _):
        return self._origin

    def co_consts(self, target):
        return tuple()

    @property
    def co_argcount(self):
        return 0

    @property
    def co_nlocals(self):
        return 0

    @property
    def co_names(self):
        return tuple()

    @property
    def co_varnames(self):
        return tuple()
