from model import *
def add_return(program : Program) -> Program:
    return Program([add_fn_return(s) for s in program.statements])

def add_fn_return(statement : Statement) -> Statement:
    if isinstance(statement, FunctionDefinition):
        name = statement.name
        parameters = statement.parameters
        body = statement.body
        if body == [] or not isinstance(body[-1], Return):
            statement = FunctionDefinition(name, parameters, body + [Return(Integer(0))])
    return statement