# llvmformat.py

from instructionsmodel import *
indent = '    '

def llvm_format(program : Program) -> str:
    lines = ['declare i32 @_print_int(i32)\n']
    for s in program.statements:
        match s:
            case FunctionDefinition(name, parameters, body):
                definitions = f'define i32 @{name.string}('
                params_str = [f'i32 %{p.string}' for p in parameters.data]
                definitions += ", ".join(params_str) + ") {"
                lines.append(definitions)
                for block in body:
                    lines.append(f'{block.label}:')
                    for llvm_op in block.instructions:
                        lines.append(indent + llvm_op.op)
                lines.append('}\n')
            case GlobalVarDec(name):
                string = name.string
                lines.append(f'@{string} = global i32 0')
    return '\n'.join(lines)