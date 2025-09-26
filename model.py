from dataclasses import dataclass, field
from enum import Enum

# Everything EXCEPT for literal information and types will inherit from ASTNode
# Then to traverse the tree, we take the class attributes which are 
# 1. Literals (e.g. int, string) 2. ASTNodes 3. Lists (of ASTNodes)
class ASTNode: pass
class Statement(ASTNode): pass # Statements perform some operation, but do not evaluate to anything

@dataclass
class Expression(ASTNode): # Expressions MUST evaluate to some value
    wtype : str

# Top level program class
@dataclass
class Program(ASTNode):
    statements : list[Statement]

# Expressions
@dataclass
class Integer(Expression): 
    wtype : str = "int"
    n : int = 0
    __match_args__ = ('n',)
    def __init__(self, n):
        self.n = n

@dataclass
class Float(Expression): 
    wtype : str = "float"
    n : float = 0.0
    __match_args__ = ('n',)
    def __init__(self, n):
        self.n = n

@dataclass
class Character(Expression): 
    wtype : str = "char"
    c : str = ' '
    __match_args__ = ('c',)
    def __init__(self, c):
        self.c = c

# Identifiers:
# Identifiers (vars & functions) -> Identifiers (funcs) & Global/LocalId (Vars)
@dataclass
class Identifier(Expression):
    string : str
    __match_args__ = ('string',)
    def __hash__(self):
        return hash(self.string)
    def __eq__(self, other):
        return isinstance(other, Identifier) and self.string == other.string
    def __str__(self):
        return self.string

@dataclass
class GlobalId(Identifier):
    __match_args__ = Identifier.__match_args__

@dataclass
class LocalId(Identifier):
    __match_args__ = Identifier.__match_args__

@dataclass
class BinaryOp(Expression):
    op : str
    left : Expression
    right : Expression
    __match_args__ = ('op', 'left', 'right')

@dataclass
class UnaryOp(Expression):
    op : str
    exp : Expression
    __match_args__ = ('op', 'exp')

# Should parameters be a separate object
# or should it just exist within the function object?
# if we want to deal with type declarations later, how do we do that?
@dataclass
class Parameters(Expression): 
    data : list[Identifier]
    __match_args__ = ('data',)

@dataclass 
class FunctionCall(Expression):
    name : Identifier
    arguments : list[Expression]
    __match_args__ = ('name', 'arguments')

@dataclass
class Print(Statement):
    value : Expression

@dataclass
class ExprStatement(Statement):
    exp : Expression

# Variable Declarations
# AST Transformation: Variable -> Variable Decl -> Local/Global resolution
@dataclass
class Variable(Statement): 
    name : Identifier
    value : Expression

@dataclass
class VariableDeclaration(Statement):
    name : Identifier

@dataclass
class GlobalVarDec(VariableDeclaration): pass

@dataclass
class LocalVarDec(VariableDeclaration): pass

@dataclass
class Assignment(Statement):
    name : Identifier
    value : Expression

@dataclass
class If(Statement):
    test : Expression 
    consequence : list[Statement]
    alternative : list[Statement]

@dataclass
class While(Statement):
    test : Expression
    body : list[Statement]

@dataclass
class FunctionDefinition(Statement):
    name : Identifier
    parameters : Parameters
    body : list[Statement]

@dataclass
class Return(Statement):
    value : Expression = field(default_factory = Integer)