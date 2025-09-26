# controlflow.py

from model import *
from instructionsmodel import *

# Label count
count = 0
# Every label made at this stage will begin with B

def get_label():
    global count
    count += 1
    return count - 1

def add_control_flow(program : Program) -> Program:
    global count
    count = 0
    return Program(control_statements(program.statements))
    
# This is the top-level of the program, so every statement here will be a global var declaration
# or a function declaration.
def control_statements(statements : list[Statement]) -> list[Statement]:
    out = []
    for s in statements:
        if isinstance(s, GlobalVarDec):
            out.append(s)
        elif isinstance(s, FunctionDefinition):
            if len(s.body) == 1:
                out.append(s)
            else:
                out.append(FunctionDefinition(s.name, s.parameters, 
                                              statements_to_blocks(s.body[:-1], s.body[-1]) + [s.body[-1]]))
        else:
            raise RuntimeError(f'Unexpected statement type {s} when linking blocks')
    return out

# Due to preprocessing, we are guaranteed that the last statement in the function body is a return
# Furthermore, every statement in the function body at this point is either a BLOCK, If, or While
# For each BLOCK, we need to insert a GOTO
# For each If, we need to provide CBRANCH(true block, false block)
# For each While, we need to provide CBRANCH(body, post-loop)
# Iterate backwards through the blocks, passing the destination block to earlier blocks
# Key idea: When we process the If statement consequence and alternative blocks,
# we need to provide a destination for these blocks, which is outside the scope of the original if statement
# and requires use of a stack to keep track of successive exit points for nested blocks
# We can implement the stack functionality explicitly or implicitly
# The destination MUST be another block, which means that when we process a conditional test,
# the destination blocks must already be defined. However, the destination blocks may be OTHER
# If/While statements, which are not yet converted to blocks
# We can either turn these all to blocks first, but this would require extra bookkeeping for nested levels
# Alternatively, if we process backwards, then we are guaranteed the future block is already a block.
# returns a list of BLOCKs, forward direction
def statements_to_blocks(statements : list[Statement], next_block : BLOCK) -> list[Statement]: 
    if statements == []:
        return [BLOCK(f'B{get_label()}', [GOTO(next_block)])]
    # each statement here is a BLOCK, IF, or WHILE
    new_statements = []
    for statement in statements[-1::-1]:
        match statement:
            case BLOCK():
                new_statements.append(BLOCK(statement.label, statement.instructions + [GOTO(next_block)]))
                next_block = new_statements[-1]
            case If(test, consequence, alternative):
                consequence_blocks = statements_to_blocks(consequence, next_block)
                alternative_blocks = statements_to_blocks(alternative, next_block)
                test_block = BLOCK(f'B{get_label()}', test.instructions + [CBRANCH(consequence_blocks[0], alternative_blocks[0])])
                new_statements = new_statements + alternative_blocks[::-1] + consequence_blocks[::-1] + [test_block]
                next_block = new_statements[-1]
            case While(test, body):
                test_block = BLOCK("", []) # dummy
                body_blocks = statements_to_blocks(body, test_block)
                test_block.label = f'B{get_label()}'
                test_block.instructions = test.instructions + [CBRANCH(body_blocks[0], next_block)]
                new_statements = new_statements + body_blocks[::-1] + [test_block]
                next_block = new_statements[-1]
    new_statements.reverse()
    return new_statements