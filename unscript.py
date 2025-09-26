# unscript.py
from model import *
def unscript_toplevel(program : Program) -> Program:
    # Split the top-level program into three categories:
    # Global variable declarations
    # Function declarations
    # Main
    declarations = []
    functions = []
    main_statements = []
    for s in program.statements:
        match s:
            case FunctionDefinition():
                functions.append(s)
            case GlobalVarDec():
                declarations.append(s)
            case _:
                main_statements.append(s)
    functions.append(FunctionDefinition(Identifier("", 'main'), Parameters("", []),
                                        main_statements))
    return Program(declarations + functions)
    