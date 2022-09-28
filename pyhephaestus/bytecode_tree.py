import dis

from collections import deque

from .constants import LOAD_BUILD_CLASS, MAKE_FUNCTION
from .declaration import FunctionDeclaration, ClassDeclaration, Declaration
from .instruction import HephaestusInstruction


def func_bytecode(func_code):
    return bytecode_tree(
        FunctionDeclaration(
            func_code.co_name,
            func_code,
            instructions=list(map(HephaestusInstruction, dis.get_instructions(func_code))),
        )
    )


def bytecode_tree(root: Declaration) -> Declaration:
    todo = deque([root])

    while todo:
        item = todo.popleft()

        instructions_list = item.instruction_list
        for index, instruction in enumerate(instructions_list):
            if instruction.opname == LOAD_BUILD_CLASS:
                todo.append(
                    declaration := ClassDeclaration(
                        name=instructions_list[index + 1].argval.co_name,
                        code_object=instructions_list[index + 1].argval,
                        instructions=list(map(
                            HephaestusInstruction,
                            dis.get_instructions(instructions_list[index + 1].argval))
                        )
                    )
                )
                item.children.append(declaration)

            if instruction.opname == MAKE_FUNCTION:
                if instructions_list[index - 3].opname == LOAD_BUILD_CLASS:
                    continue

                todo.append(
                    declaration := FunctionDeclaration(
                        name=instructions_list[index - 2].argval.co_name,
                        code_object=instructions_list[index - 2].argval,
                        instructions=list(map(
                            HephaestusInstruction,
                            dis.get_instructions(instructions_list[index - 2].argval))
                        )
                    )
                )
                item.children.append(declaration)

    return root


def debug_build_tree(root, indent=''):
    buffer = ''
    buffer += indent + repr(root) + '\n'
    for children in root.child:
        buffer += debug_build_tree(children, indent + '    ')

    return buffer
