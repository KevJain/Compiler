from model import *
from instructionsmodel import *

indent = '    '

def format_program(program : Program) -> str:
    return format_statements(program.statements, 0)

def format_statements(statements : list[Statement], indent_level) -> str:
    code = ''
    for s in statements:
        code += indent * indent_level + format_statement(s, indent_level)
    return code

def format_expression(e : Expression) -> str:
    match e:
        case Integer(n):
            return str(n)
        case Float(n):
            return str(n)
        case Character(c):
            return c
        case GlobalId(string = string):
            return f'global[{string}]'
        case LocalId(string = string):
            return f'local[{string}]'
        case Identifier(s):
            return s
        case BinaryOp(op, left, right):
            return f'{format_expression(left)} {op} {format_expression(right)}'
        case UnaryOp(op, exp):
            return f'-{format_expression(exp)}'
        case Parameters(data):
            return ", ".join([format_expression(v) for v in data])
        case FunctionCall(name, arguments):
            return f'{format_expression(name)}({", ".join([format_expression(a) for a in arguments])})'
        case EXPR():
            return str(e)
        case _:
            raise RuntimeError(f'Can\'t format {e}')
    


def format_statement(s : Statement, level) -> str:
    match s:
        case Print(value):
            return f'print {format_expression(value)};\n'
        case Variable(name, value):
            return f'var {format_expression(name)} = {format_expression(value)};\n'
        case GlobalVarDec(name):
            return f'global {format_expression(name)};\n'
        case LocalVarDec(name):
            return f'local {format_expression(name)};\n'
        case VariableDeclaration(name):
            return f'var {format_expression(name)};\n'
        case Assignment(name, value):
            return f'{format_expression(name)} = {format_expression(value)};\n'
        case If(test, consequence, alternative):
            code =  f'if {format_expression(test)} {{ \n'
            code += format_statements(consequence, level + 1)
            if alternative != []:
                code += indent *level + f'}} else {{\n'
                code += format_statements(alternative, level + 1)
                code += indent * level + f'}}\n'
            else:
                code += indent * level + "}\n"
            return code
        case While(test, body):
            code = f'while {format_expression(test)} {{ \n'
            code += format_statements(body, level + 1)
            code += indent * level + f'}}\n'
            return code 
        case FunctionDefinition(name, parameters, body):
            code = f'func {format_expression(name)}({format_expression(parameters)}) {{\n'
            code += format_statements(body, level + 1)
            code += indent * level + f'}}\n'
            return code
        case Return(value):
            return f'return {format_expression(value)};\n'
        case STATEMENT():
            code = '[\n'
            for ins in s.instructions:
                code += indent * (level + 1) + str(ins) + '\n'
            code += indent * level + ']\n'
            return code
        case BLOCK(label, instructions):
            code = f"Block: {label}\n"
            for ins in instructions:
                code += indent * (level + 1) + str(ins) + '\n'
            return code
        case ExprStatement(exp):
            return format_expression(exp) + '\n'
        case _:
            raise RuntimeError(f'Can\'t format {s}')


