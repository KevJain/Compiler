from model import *

def deinit_variables(program : Program) -> Program:
    return Program(deinit_statements(program.statements))

def deinit_statements(statements : list[Statement]) -> list[Statement]:
    out = []
    for s in statements:
        match s:
            case Variable(name, value): # TODO: Create typed assignment
                out.append(VariableDeclaration(name))
                out.append(Assignment(name, value))
            case If(test, consequence, alternative):
                out.append(If(test, 
                              deinit_statements(consequence),
                              deinit_statements(alternative)))
            case While(test, body):
                out.append(While(test,
                                 deinit_statements(body)))
            case FunctionDefinition(name, parameters, body):
                out.append(FunctionDefinition(name, parameters,
                                              deinit_statements(body)))
            case _:
                out.append(s)
    return out