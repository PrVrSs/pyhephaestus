from types import CodeType


class Declaration:
    def __init__(self, name: str, code_object: CodeType, instructions: list):
        self._method_name = name
        self._code_object = code_object
        self._instructions = instructions

        self.children: list[Declaration] = []

    @property
    def instruction_list(self):
        return self._instructions

    def __repr__(self) -> str:
        raise NotImplementedError


class ImportDeclaration(Declaration):
    def __repr__(self) -> str:
        return ''


class ModuleDeclaration(Declaration):
    def __repr__(self) -> str:
        return ''


class ClassDeclaration(Declaration):
    def __repr__(self) -> str:
        return f'ClassDeclaration(name={self._method_name}, code={self._code_object})'


class FunctionDeclaration(Declaration):
    def __repr__(self) -> str:
        return f'FunctionDeclaration(name={self._method_name}, code={self._code_object})'


class FieldDeclaration(Declaration):
    def __repr__(self) -> str:
        return 'FieldDeclaration()'
