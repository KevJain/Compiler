# resolve.py

from model import *
class Scope():
    def __init__(self, parent = None, top_level = False):
        self.parent = parent
        self.levels = {} # identifier : (scope, type)
        self.top_level = top_level

    def declare(self, identifier : Identifier):
        self.levels[identifier.string] = ('global' if self.top_level else 'local', 
                                          identifier.wtype)

    def lookup(self, identifier : Identifier):
        if identifier.string in self.levels:
            return self.levels[identifier.string]
        elif self.parent != None:
            return self.parent.lookup(identifier)
        else:
            raise RuntimeError(f'{identifier} is undefined')

def resolve_scopes(program : Program) -> Program:
    # find globals:
    global_scope = Scope(top_level = True)
    # get function types:
    for s in program.statements:
        if isinstance(s, FunctionDefinition):
            global_scope.declare(s.name)
    return Program(resolve_statements_scope(program.statements, global_scope))

def resolve_statements_scope(statements : list[Statement], scope : Scope) -> list[Statement]:
    out = []
    for s in statements:
        out.append(resolve_statement_scope(s, scope))
    out = resolve_types_in_declar(out, scope)
    return out

def resolve_types_in_declar(statements : list[Statement], scope : Scope) -> list[Statement]:
    out = []
    for s in statements:
        if isinstance(s,VariableDeclaration):
            if scope.top_level:
                out.append(GlobalVarDec(Identifier(scope.lookup(s.name), s.name.string)))
            else:
                out.append(LocalVarDec(Identifier(scope.lookup(s.name), s.name.string)))
        else:
            out.append(s)
    return out

def resolve_statement_scope(statement : Statement, scope : Scope) -> Statement:
    match statement:
        case Print(value):
            return Print(resolve_expression_scope(value, scope))
        case VariableDeclaration(name):
            scope.declare(name)
            if scope.top_level:
                return GlobalVarDec(name)
            else:
                return LocalVarDec(name)
        case Assignment(name, value):
            assign_value = resolve_expression_scope(value, scope)
            if scope.lookup(name)[1] == "":
                scope.declare(Identifier(assign_value.wtype, name.string))
            elif scope.lookup(name)[1] != assign_value.wtype:
                raise RuntimeError(f'Mismatched types between {name} and {assign_value}')
            return Assignment(resolve_expression_scope(name, scope), 
                            assign_value)
        case If(test, consequence, alternative):
            return If(resolve_expression_scope(test, scope),
                    resolve_statements_scope(consequence, Scope(scope)),
                    resolve_statements_scope(alternative, Scope(scope)))
        case While(test, body):
            return While(resolve_expression_scope(test, scope),
                        resolve_statements_scope(body, Scope(scope)))
        case FunctionDefinition(name, parameters, body):
            func_scope = Scope(scope)
            for param in parameters.data:
                func_scope.declare(param)
            return FunctionDefinition(name, parameters,
                                    resolve_statements_scope(body, func_scope))
        case Return(value):
            return Return(resolve_expression_scope(value, scope))
        case ExprStatement(value):
            return ExprStatement(resolve_expression_scope(value, scope))
        case _:
            raise RuntimeError(f"Can't resolve scope of statement {statement}")

def resolve_expression_scope(expression : Expression, scope : Scope) -> Expression:
    match expression:
        case Identifier(string):
            e_scope, e_type = scope.lookup(expression)
            if e_scope == 'global':
                return GlobalId(e_type, string)
            else:
                return LocalId(e_type, string)
        case BinaryOp(op, left, right):
            resolved_left = resolve_expression_scope(left, scope)
            resolved_right = resolve_expression_scope(right, scope)
            if resolved_left.wtype != resolved_right.wtype:
                raise SyntaxError(f'Mismatched types for {op} at {expression}, got {resolved_left.wtype } and {resolved_right.wtype }')
            return BinaryOp(resolved_left.wtype, op, resolved_left, resolved_right)
        case UnaryOp(op, exp):
            resolved_exp = resolve_expression_scope(exp, scope)
            if resolved_exp.wtype == 'int':
                return BinaryOp('int', op, Integer(0), resolved_exp)
            elif resolved_exp.wtype == 'float':
                return BinaryOp('float', op, Float(0.0), resolved_exp)
            else:
                raise RuntimeError(f'Unknown type for {exp}')
        case FunctionCall(name, arguments):
            return_type = scope.lookup(name)[1]
            return FunctionCall(return_type, 
                                Identifier(return_type, name.string), 
                                [resolve_expression_scope(e, scope) for e in arguments])
        case _:
            return expression
            

                

    
    
