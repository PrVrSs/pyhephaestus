from .bytecode_tree import HephaestusInstruction
from .visitors import BytecodeVisitor, DeclarationVisitor, Visitor


class BytecodeWrapper:
    def __init__(self, instructions: list[HephaestusInstruction]):
        self._instructions = instructions
        self._bytecode_tree = None

    def accept(self, visitor: Visitor) -> None:
        match visitor:
            case BytecodeVisitor():
                visitor.visit(self._instructions)
            case DeclarationVisitor():
                visitor.visit(self._bytecode_tree)
            case _:
                raise TypeError('Unknown visitor')
