# instructionmodel.py
from model import *

"""   Assume we have a VM that supports the following instructions:
PUSH(value)         # Push a new value on the stack
ADD()               # +
MUL()               # *
LT()                # <
EQ()                # ==
LOAD_GLOBAL(name)   # Load global variable into stack
LOAD_LOCAL(name)    # Load local variable into stack
CALL(name, n)       # Call function name with n arguments
"""

# VM definitions
@dataclass
class INSTRUCTION: pass

@dataclass
class PUSH(INSTRUCTION):
    value : int
    def __str__(self):
        return f'PUSH({self.value})'
    
@dataclass
class POP(INSTRUCTION): pass

@dataclass
class ARITHMETIC(INSTRUCTION): pass

@dataclass
class RELATION(INSTRUCTION): pass

@dataclass
class ADD(ARITHMETIC): pass

@dataclass
class MINUS(ARITHMETIC): pass

@dataclass
class MULT(ARITHMETIC): pass

@dataclass
class DIVIDE(ARITHMETIC): pass

@dataclass
class LT(RELATION): pass

@dataclass
class LE(RELATION): pass

@dataclass
class GT(RELATION): pass

@dataclass
class GE(RELATION): pass

@dataclass
class EQ(RELATION): pass

@dataclass
class NE(RELATION): pass

@dataclass
class LOAD_GLOBAL(INSTRUCTION):
    name : str
    def __str__(self):
        return f'LOAD_GLOBAL({self.name})'

@dataclass
class LOAD_LOCAL(INSTRUCTION):
    name : str
    def __str__(self):
        return f'LOAD_LOCAL({self.name})'

@dataclass
class CALL(INSTRUCTION):
    name : str
    return_type : str
    args : list[str]
    def __str__(self):
        return f'CALL({self.name}, {self.num_args})'

@dataclass
class STORE_GLOBAL(INSTRUCTION):
    name : str
    def __str__(self):
        return f'STORE_GLOBAL({self.name})'

@dataclass
class STORE_LOCAL(INSTRUCTION):
    name : str
    def __str__(self):
        return f'STORE_LOCAL({self.name})'

@dataclass
class PRINT(INSTRUCTION):
    def __str__(self):
        return 'PRINT'

@dataclass
class LOCAL(INSTRUCTION):
    name : str
    def __str__(self):
        return f'LOCAL({self.name})'

@dataclass
class RETURN(INSTRUCTION):
    def __str__(self):
        return 'RETURN'

@dataclass
class FPUSH(INSTRUCTION):
    value : int
    def __str__(self):
        return f'PUSH({self.value})'
    
@dataclass
class FARITHMETIC(INSTRUCTION): pass

@dataclass
class FRELATION(INSTRUCTION): pass

@dataclass
class FADD(ARITHMETIC): pass

@dataclass
class FMINUS(ARITHMETIC): pass

@dataclass
class FMULT(ARITHMETIC): pass

@dataclass
class FDIVIDE(ARITHMETIC): pass

@dataclass
class FLT(RELATION): pass

@dataclass
class FLE(RELATION): pass

@dataclass
class FGT(RELATION): pass

@dataclass
class FGE(RELATION): pass

@dataclass
class FEQ(RELATION): pass

@dataclass
class FNE(RELATION): pass

@dataclass
class FLOAD_GLOBAL(INSTRUCTION):
    name : str
    def __str__(self):
        return f'LOAD_GLOBAL({self.name})'

@dataclass
class FLOAD_LOCAL(INSTRUCTION):
    name : str
    def __str__(self):
        return f'LOAD_LOCAL({self.name})'

@dataclass
class FSTORE_GLOBAL(INSTRUCTION):
    name : str
    def __str__(self):
        return f'STORE_GLOBAL({self.name})'

@dataclass
class FSTORE_LOCAL(INSTRUCTION):
    name : str
    def __str__(self):
        return f'STORE_LOCAL({self.name})'

@dataclass
class FPRINT(INSTRUCTION):
    def __str__(self):
        return 'PRINT'

@dataclass
class FLOCAL(INSTRUCTION):
    name : str
    def __str__(self):
        return f'LOCAL({self.name})'

@dataclass
class FRETURN(INSTRUCTION):
    def __str__(self):
        return 'RETURN'

@dataclass
class GOTO(INSTRUCTION):
    destination : 'BLOCK'
    def __str__(self):
        return f'GOTO({self.destination.label})'

@dataclass
class CBRANCH(INSTRUCTION):
    true_block : 'BLOCK'
    false_block : 'BLOCK'
    def __str__(self):
        return f'CBRANCH({self.true_block.label}, {self.false_block.label})'

# Model extensions:
@dataclass
class EXPR(Expression):
    instructions : list[INSTRUCTION]
    def __init__(self, instructions):
        self.wtype = 'EXPR'
        self.instructions = instructions
    def __str__(self):
        return f'[{", ".join([str(ins) for ins in self.instructions])}]'
    
@dataclass
class STATEMENT(Statement):
    instructions : list[INSTRUCTION]
    def __str__(self):
        return f'[{", ".join([str(ins) for ins in self.instructions])}]'
    
@dataclass
class BLOCK(Statement):
    label : str
    instructions : list[INSTRUCTION]

@dataclass
class LLVM(INSTRUCTION):
    op : str
    def __str__(self):
        return f'LLVM({self.op})'