# llvmentry.py
from instructionsmodel import *

def create_entry_blocks(program : Program) -> Program:
    new_statements = []
    for s in program.statements:
        if isinstance(s, FunctionDefinition):
            new_statements.append(add_entry_to_function(s))
        else:
            new_statements.append(s)
    return Program(new_statements)

def add_entry_to_function(function : FunctionDefinition) -> FunctionDefinition:
    entry_block_ins = []
    new_params = []
    for param in function.parameters.data:
        name = param.string
        new_params.append(Identifier("", f'.arg_{name}'))
        entry_block_ins.append(LLVM(f'%{name} = alloca i32'))
        entry_block_ins.append(LLVM(f'store i32 %.arg_{name}, i32* %{name}'))

    entry_block_ins.append(LLVM(f'br label %{function.body[0].label}'))
    return FunctionDefinition(function.name, Parameters("", new_params), [BLOCK('entry', entry_block_ins)] + function.body)
