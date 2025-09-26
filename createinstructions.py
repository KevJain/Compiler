# expressiontoinstruct.py

from instructionsmodel import *
from model import *

def exps_stmts_to_instr(program : Program) -> Program:
    return Program(convert_statements(program.statements))

def convert_statements(statements : list[Statement]) -> list[Statement]:
    return [statement_to_instructions(s) for s in statements]

def statement_to_instructions(s : Statement) -> Statement:
    match s:
        case Print(e):
            value = expression_to_instructions(e)
            return STATEMENT(value.instructions + [get_print(e)])
        case Assignment(name, e):
            value = expression_to_instructions(e)
            return STATEMENT(value.instructions + [get_assignment(name, e)])
        case If(test, consequence, alternative):
            return If(expression_to_instructions(test), convert_statements(consequence), convert_statements(alternative))
        case While(test, body):
            return While(expression_to_instructions(test), convert_statements(body))
        case FunctionDefinition(name, parameters, body):
            return FunctionDefinition(name, parameters, convert_statements(body))
        case Return(e):
            value = expression_to_instructions(e)
            return STATEMENT(value.instructions + [get_return(e)])
        case LocalVarDec(name):
            return STATEMENT([get_local_dec(name)])
        case ExprStatement(e):
            return STATEMENT(expression_to_instructions(e).instructions + [POP()])
        case _:
            return s

def get_print(e : Expression) -> INSTRUCTION:
    match e.wtype:
        case 'int':
            return PRINT()
        case 'float':
            return FPRINT()
        case _:
            raise RuntimeError(f'Unknown type for print {e}')
    
def get_assignment(name : Identifier, e : Expression) -> INSTRUCTION:
    if isinstance(name, GlobalId):
        if name.wtype == 'int':
            return STORE_GLOBAL(name.string)
        elif name.wtype == 'float':
            return FSTORE_GLOBAL(name.string)
        else:
            raise RuntimeError(f'Unknown type for assignment {name} {GlobalId}')
    elif isinstance(name, LocalId):
        if name.wtype == 'int':
            return STORE_LOCAL(name.string)
        elif name.wtype == 'float':
            return FSTORE_LOCAL(name.string)
        else: 
            raise RuntimeError(f'Unknown type for assignment {name} {GlobalId}')
    else:
        raise RuntimeError(f'Unkown type for assignment {name}')

def get_return(e : Expression) -> INSTRUCTION:
    match e.wtype:
        case 'int':
            return RETURN()
        case 'float':
            return FRETURN()
        case _:
            raise RuntimeError(f'Unknown type for return {e}')

def get_local_dec(name : Identifier) -> INSTRUCTION:
    match name.wtype:
        case 'int':
            return LOCAL(name.string)
        case 'float':
            return FLOCAL(name.string)
        case _:
            raise RuntimeError(f'Unknown type for local declaration {name}')

def expression_to_instructions(expr : Expression) -> EXPR:
    match expr:
        case Integer(n):
            return EXPR([PUSH(n)])
        case Float(n):
            return EXPR([FPUSH(n)])
        case GlobalId(string, wtype=wtype):
            if wtype == 'int':
                return EXPR([LOAD_GLOBAL(string)])
            elif wtype == 'float':
                return EXPR([FLOAD_GLOBAL(string)])
            else:
                raise RuntimeError(f'Unknown type for {expr}')
        case LocalId(string, wtype=wtype):
            if wtype == 'int':
                return EXPR([LOAD_LOCAL(string)])
            elif wtype == 'float':
                return EXPR([FLOAD_LOCAL(string)])
            else:
                raise RuntimeError(f'Unknown type for {expr}')
        case BinaryOp(op, left, right):
            left_instr = expression_to_instructions(left)
            right_instr = expression_to_instructions(right)
            op_instr = ""
            match op:
                case '+':
                    op_instr = 'ADD'
                case '-':
                    op_instr = 'MINUS'
                case '*':
                    op_instr = 'MULT'
                case '/':
                    op_instr = 'DIVIDE'
                case '<':
                    op_instr = 'LT'
                case '<=':
                    op_instr = 'LE'
                case '>':
                    op_instr = 'GT'
                case '>=':
                    op_instr = 'GE'
                case '==':
                    op_instr = 'EQ'
                case '!=':
                    op_instr = 'NE'
                case _:
                    raise RuntimeError(f'Unknown operation {op} found')
            if expr.wtype == 'float':
                op_instr = 'F' + op_instr
            return EXPR(left_instr.instructions + 
                        right_instr.instructions + [globals()[op_instr]()])
        case FunctionCall(name, arguments):
            args_exprs = [expression_to_instructions(a) for a in arguments]
            args_instr = [instr for exp in args_exprs for instr in exp.instructions ]
            args_types = [a.wtype for a in arguments]
            return EXPR(args_instr + [CALL(name.string, name.wtype, args_types)])
        



def test_expr_instr():
    tests = [BinaryOp("", '+', Integer(0), LocalId('x')),
             GlobalId("", 'y'),
             BinaryOp("", '+', BinaryOp('+', LocalId('x'), Integer(1)), LocalId('x'))]

    for test in tests:
        print(expression_to_instructions(test))

#test_expr_instr()