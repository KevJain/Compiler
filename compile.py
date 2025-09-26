# compile.py

from model import *
from tokenizer import tokenize
from parser import Parser
from main import compile
from llvmformat import llvm_format
from formatter import format_program
import sys
import os

def file_to_AST(filename : str) -> Program:
    with open(filename, 'r') as file:
        src = file.read()
    tokens = tokenize(src)
    program = Program(Parser(tokens).parse_statements())
    return program

def main():
    filename = sys.argv[1]
    output = sys.argv[2]
    syntax_tree = file_to_AST(f'tests/{filename}')
    simplified_tree = compile(syntax_tree)
    #print(format_program(simplified_tree))
    out = llvm_format(simplified_tree)
    print(out)
    with open("temp.ll", 'w') as file:
        file.write(out)
    print(f"Created llvm output file")
    os.system(f'clang temp.ll runtime.c -o {output}')
    print(f'Compiled {filename} to {output}')

if __name__ == '__main__':
    main()