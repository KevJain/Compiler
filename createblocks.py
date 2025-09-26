# createblocks.py

from model import *
from instructionsmodel import *

count = 0

def create_blocks(program : Program) -> Program:
    global count
    count = 0
    return Program(create_blocks_statements(program.statements))


def create_blocks_statements(statements : list[Statement]) -> list[Statement]:
    global count
    out = []
    cur_block = []
    for s in statements:
        if isinstance(s, GlobalVarDec):
            out.append(s)
        if isinstance(s, STATEMENT):
            cur_block.append(s)
        else:
            if cur_block:
                label = f'L{count}'
                count += 1
                out.append(BLOCK(label, [ins for statement in cur_block for ins in statement.instructions]))
                cur_block = []
            match s:
                case If(test, consequence, alternative):
                    out.append(If(test, 
                               create_blocks_statements(consequence), 
                               create_blocks_statements(alternative)))
                case While(test, body):
                    out.append(While(test, create_blocks_statements(body)))
                case FunctionDefinition(name, parameters, body):
                    out.append(FunctionDefinition(name, parameters,
                                                  create_blocks_statements(body)))
    if cur_block:
        label = f'L{count}'
        count += 1
        out.append(BLOCK(label, [ins for statement in cur_block for ins in statement.instructions]))
    return out
