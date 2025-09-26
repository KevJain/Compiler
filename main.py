from model import *
from formatter import format_program
from foldconstants import fold_constants # type: ignore
from deinit import deinit_variables # type: ignore
from resolve import resolve_scopes # type: ignore
from unscript import unscript_toplevel # type: ignore
from addreturn import add_return # type: ignore
from parser import *
from createblocks import create_blocks
from controlflow import add_control_flow
from createinstructions import exps_stmts_to_instr
from LLVMgen import llvm_make
from llvmentry import create_entry_blocks
from llvmformat import llvm_format

def init_programs():
    programs = []
    programs.append(Program([
        Variable(Identifier('x'), Integer(10)),
        Assignment(Identifier('x'), BinaryOp('+', Identifier('x'), Integer(1))),
        Print(BinaryOp('+', BinaryOp('*', Integer(23), Integer(45)), Identifier('x')))
    ]))
    programs.append(Program([
        Variable(Identifier('x'), Integer(3)),
        Variable(Identifier('y'), Integer(4)),
        Variable(Identifier('min'), Integer(0)),
        If(BinaryOp('<', Identifier('x'), Identifier('y')),
           [Assignment(Identifier('min'), Identifier('x'))],
           [Assignment(Identifier('min'), Identifier('y'))]
           ),
        Print(Identifier('min'))
    ]))
    programs.append(Program([
        Variable(Identifier('result'), Integer(1)),
        Variable(Identifier('x'), Integer(1)),
        While(BinaryOp('<', Identifier('x'), Integer(10)),
                [Assignment(Identifier('result'), 
                          BinaryOp('*', Identifier('result'), Identifier('x'))),
                Assignment(Identifier('x'),
                           BinaryOp('+', Identifier('x'), Integer(1)))
                ]),
        Print(Identifier('result'))
    ]))
    programs.append(Program([
        FunctionDefinition(Identifier("add1"),
                           Parameters([Identifier('x')]),
                           [Assignment(Identifier('x'), BinaryOp('+', Identifier('x'), Integer(1))),
                            Return(Identifier('x'))]),
        Variable(Identifier('x'), Integer(10)),
        Print(BinaryOp('+', (BinaryOp('*', Integer(23), Integer(45))),
                  FunctionCall(Identifier('add1'),[Identifier('x')]))),
        Print(Identifier('x'))
    ]))
    programs.append(Program([
        Variable(Identifier('x'), Integer(2)),
        If(BinaryOp('<', Identifier('x'), Integer(10)),
           [Variable(Identifier('y'), BinaryOp('+', Identifier('x'), Integer(1))),
            Print(Identifier('y'))],
            [])
    ]))
    programs.append(Program([
        Variable(Identifier('v'), BinaryOp('+', Integer(4), Integer(5))),
        FunctionDefinition(Identifier('square'), Parameters([Identifier('x')]),
                           [Variable(Identifier('r'), BinaryOp('*', Identifier('x'), Identifier('x'))),
                            Return(Identifier('r'))]),
        Variable(Identifier('result'), FunctionCall(Identifier('square'), [Identifier('v')])),
        Print(Identifier('result'))
    ]))
    return programs

def print_programs(programs : list[Program]):
    for i in range(len(programs)):
        print(f'Program {i + 1}:')
        print(format_program(programs[i]))

def compile(program : Program) -> Program:
    print(format_program(program))
    program = fold_constants(program)
    print(format_program(program))
    program = deinit_variables(program)
    program = resolve_scopes(program)
    program = unscript_toplevel(program)
    program = add_return(program)
    print(program)
    print(format_program(program))
    program = exps_stmts_to_instr(program)
    program = create_blocks(program)
    program = add_control_flow(program)
    print(format_program(program))
    program = llvm_make(program)
    program = create_entry_blocks(program)
    return program

def project2(programs : list[Program]) -> list[Program]:
    for i in range(len(programs)):
        print(f'Program {i + 1}:')
        print(format_program(compile(programs[i])))

def file_to_AST(filename : str) -> Program:
    with open(filename, 'r') as file:
        src = file.read()
    tokens = tokenize(src)
    program = parse_tokens(tokens)
    return program

def parse_tokens(tokens : list[Token]) -> Program:
    return Program(Parser(tokens).parse_statements())

def main():
    #programs = init_programs()
    #tests(programs)
    tests([])
    #print_programs(programs)
    #project2(programs)

def tests(programs : list[Program]):
    tests = ['program1.wb', 'program2.wb', 'program3.wb', 'program4.wb', 'fact.wb', 'factre.wb', 'unary.wb']
    for i in range(len(tests)):
        ast = file_to_AST(f'tests/wabbi/{tests[i]}')
        print(f"Testing {tests[i]}: ==========================================================================")
        #if i < 4:
            #assert programs[i] == ast, ast
        #print(format_program(compile(ast)))
        print(llvm_format(compile(ast)))
        print(f"Finished Testing {tests[i]}: ==========================================================================")

if __name__ == '__main__':
    main()
    
