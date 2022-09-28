from collections import deque
from contextlib import contextmanager
from typing import Callable, Iterator

from .declaration import Declaration


class Visitor:
    def visit(self, declaration):
        raise NotImplementedError


class BytecodeVisitor(Visitor):
    def visit(self, declaration: Declaration):
        for instruction in declaration.instruction_list:
            visitor: Callable = getattr(self, f'visit_{instruction.opname.lower()}', None)
            if visitor is None:
                continue

            yield visitor(instruction)

    def deep_visit(self, node: Declaration):
        todo = deque([node])

        while todo:
            item = todo.popleft()
            yield from self.visit(item)
            todo.extendleft(item.children)


class DeclarationVisitor(Visitor):
    def visit(self, declaration: Declaration):
        return getattr(
            self,
            f'visit_{declaration.__class__.__name__}',
            self.generic_visit,
        )(declaration)

    def generic_visit(self, node: Declaration):
        for child in node.children:
            self.visit(child)


class Listener:
    def walk(self, node: Declaration) -> None:
        with self._listener(node):
            for child in node.children:
                self.walk(child)

    @contextmanager
    def _listener(self, node: Declaration) -> Iterator[None]:
        self.enter_rule(node)
        yield
        self.exit_rule(node)

    def enter_rule(self, node: Declaration) -> None:
        raise NotImplementedError

    def exit_rule(self, node: Declaration) -> None:
        raise NotImplementedError
