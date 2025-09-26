from model import *

def fold_constants(program : Program) -> Program:
    return Program(fold_statements(program.statements))

def fold_statements(statements : list[Statement]) -> list[Statement]:
    return [fold_statement(s) for s in statements]

def fold_statement(s : Statement) -> Statement:
    match s:
        case Print(e):
            return Print(fold_expression(e))
        case Assignment(name, e):
            return Assignment(name, fold_expression(e))
        case If(test, consequence, alternative):
            return If(fold_expression(test), fold_statements(consequence), fold_statements(alternative))
        case While(test, body):
            return While(fold_expression(test), fold_statements(body))
        case FunctionDefinition(name, parameters, body):
            return FunctionDefinition(name, parameters, fold_statements(body))
        case Return(value):
            return Return(fold_expression(value))
        case ExprStatement(value):
            return ExprStatement(fold_expression(value))
        case VariableDeclaration():
            return s
        case Variable(name, value):
            return Variable(name, fold_expression(value))
        case _:
            raise RuntimeError(f"Can't fold {s}")
        
def fold_expression(e : Expression) -> Expression:
    match e:
        case BinaryOp(op, left, right):
            folded_left = fold_expression(left)
            folded_right = fold_expression(right)
            match (folded_left, folded_right):
                case (Integer(l), Integer(r)):
                    if op == '+':
                        return Integer(l+r)
                    elif op == '*':
                        return Integer(l*r)
                    elif op == '<' or '==':
                        return e
                    else:
                        raise RuntimeError(f"Unsupport operation type {op}")
                case _:
                    return BinaryOp("", op, folded_left, folded_right)
        case UnaryOp(op, exp):
            folded_exp = fold_expression(exp)
            return UnaryOp("", op, folded_exp)
        case FunctionCall(name, arguments):
            new_args = [fold_expression(exp) for exp in arguments]
            return FunctionCall(name.wtype, name, new_args)
        case _:
            return e