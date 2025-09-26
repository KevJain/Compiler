from dataclasses import dataclass

@dataclass
class Token:
    token_type : str
    value : str

symbols = {
    '+' : 'PLUS',
    '-' : 'MINUS',
    '*' : 'TIMES',
    '/' : 'DIVIDE',
    '<' : 'LT',
    '<=': 'LE',
    '>' : 'GT',
    '>=': 'GE',
    '==': 'EQ',
    '!=': 'NE',
    '=' : 'ASSIGN',
    ';' : 'SEMI',
    '(' : 'LPAREN',
    ')' : 'RPAREN',
    '{' : 'LBRACE',
    '}' : 'RBRACE',
    ',' : 'COMMA',
    '!' : 'ERRORBANG'
}

keywords = {
    'var' : 'VAR',
    'print' : 'PRINT',
    'if' : 'IF',
    'else' : 'ELSE',
    'while' : 'WHILE',
    'func' : 'FUNC',
    'return' : 'RETURN',
    'int' : 'TYPE',
    'float' : 'TYPE',
    'char' : 'TYPE'
}

def tokenize(text : str) -> list[Token]:
    def peek(n):
        if n < len(text):
            return text[n]
        return '\0'
    
    i = 0
    tokens = []
    while i < len(text):
        c = text[i]
        if c.isspace():
            i += 1
        elif c == '/': # Check for comments
            if peek(i+1) == '/':
                end_line = text.find('\n', i)
                #print(f'Skipping comment from {i} to {end_line}')
                if end_line == -1:
                    i = len(text)
                else:
                    i = end_line
                #tokens.append(Token('COMMENT', text[i:end_line]))
            else:
                tokens.append(Token('DIVIDE', '/'))
                i += 1
        elif c in symbols: # Check for symbols
            if c == '=' and peek(i + 1) == '=':
                i += 1
                tokens.append(Token('EQ', '=='))
            elif c == '<' and peek(i + 1) == '=':
                i += 1
                tokens.append(Token('LE', '<='))
            elif c == '>' and peek(i + 1) == '=':
                i += 1
                tokens.append(Token('GE', '>='))
            elif c == '!' and peek(i + 1) == '=':
                i += 1
                tokens.append(Token('NE', '!='))
            else:
                tokens.append(Token(symbols[c], c))
            i += 1
        elif c.isdigit():
            num = c
            i += 1
            while i < len(text) and text[i].isdigit():
                num += text[i]
                i += 1
            if peek(i) == '.': # float detected
                num += '.'
                i += 1
                while peek(i).isdigit():
                    num += text[i]
                    i += 1
                tokens.append(Token('FLOAT', num))
            else:
                tokens.append(Token('INTEGER', num))
        elif c == "'":
            i += 1
            char = ''
            while peek(i) != "'" and peek(i) != '\0':
                char += text[i]
                i += 1
            if peek(i) == '\0':
                raise RuntimeError(f'Unclosed char at {char}')
            #print(char)
            i += 1
            tokens.append(Token('CHAR', char))
        elif c.isalpha() or c == '_':
            word = c
            i += 1
            while i < len(text) and text[i].isalnum() or text[i] == '_':
                word += text[i]
                i += 1
            if word in keywords:
                tokens.append(Token(keywords[word], word))
            else:
                tokens.append(Token('NAME', word))
        else:
            raise RuntimeError(f"Can't match {c} in {text}")

    tokens.append(Token('EOF', ''))
    return tokens

def test_symbols():
    print(tokenize("abc abc123"))
    print(tokenize("+ - * / < <= > >= == != = ; ( ) { } ,"))
    print(tokenize('print 123 + xy;'))
    print(tokenize('==='))
    print(tokenize('if a < b { statement1; statement2;} else {statement3;statement4;}'))
    print(tokenize('else if func print return var while elsee'))

def tokenize_programs():
    file_names = ['fact.wb', 'program1.wb']
    for name in file_names:
        with open(f'tests/{name}', 'r') as file:
            src = file.read()
        
        print(tokenize(src))

#test_symbols()
#tokenize_programs()