# parser.py

from tokenizer import * #type: ignore
from model import *

class Parser:
    def __init__(self, tokens : list[Token]):
        self.tokens = tokens
        self.n = 0

    def expect(self, token_type : str) -> Token: # Where token_type is one of the valid types in the grammar
        token = self.tokens[self.n]
        if token.token_type == 'EOF':
            raise SyntaxError(f'Expected {token_type} but reached EOF')
        elif token.token_type == token_type:
            self.n += 1
            return token
        else:
            raise SyntaxError(f'Expected {token_type} at {token}')

    # hand-written statement parsing:
    def parse_print(self) -> Print:
        self.expect('PRINT')
        value = self.parse_expression()
        self.expect('SEMI')
        return Print(value)
    
    def parse_variable_definition(self) -> Variable:
        self.expect('VAR')
        name = self.expect('NAME').value
        if self.peek().token_type == 'ASSIGN':
            self.expect('ASSIGN')
            value = self.parse_expression()
            self.expect('SEMI')
            return Variable(Identifier(value.wtype, name), value)
        else:
            wtype = self.expect('TYPE').value
            self.expect('SEMI')
            return VariableDeclaration(Identifier(wtype, name))

    def parse_assignment(self) -> Assignment:
        name_token = self.expect('NAME')
        self.expect('ASSIGN')
        value = self.parse_expression()
        self.expect('SEMI')
        return Assignment(Identifier("", name_token.value), value)

    def parse_if(self) -> If:
        self.expect('IF')
        test = self.parse_expression()
        self.expect('LBRACE')
        consequence = self.parse_statements()
        self.expect('RBRACE')
        if self.peek().token_type == 'ELSE':
            self.expect('ELSE')
            self.expect('LBRACE')
            alternative = self.parse_statements()
            self.expect('RBRACE')
        else:
            alternative = []
        return If(test, consequence, alternative)
    
    def parse_while(self) -> While:
        self.expect('WHILE')
        test = self.parse_expression()
        self.expect('LBRACE')
        body = self.parse_statements()
        self.expect('RBRACE')
        return While(test, body)
    
    def parse_func(self) -> FunctionDefinition:
        self.expect('FUNC')
        name_token = self.expect('NAME')
        self.expect('LPAREN')
        parameters = self.parse_parameters()
        self.expect('RPAREN')
        return_type = self.expect('TYPE').value
        self.expect('LBRACE')
        body = self.parse_statements()
        self.expect('RBRACE')
        return FunctionDefinition(Identifier(return_type, name_token.value), parameters, body)

    def parse_return(self) -> Return:
        self.expect('RETURN')
        value = self.parse_expression()
        self.expect('SEMI')
        return Return(value)

    def parse_parameters(self) -> Parameters:
        params = []
        if self.peek().token_type == 'RPAREN':
            return Parameters("", [])
        first_param_name = self.expect('NAME').value
        first_param_type = self.expect('TYPE').value
        params.append(Identifier(first_param_type, first_param_name))
        while self.peek().token_type == 'COMMA':
            self.expect('COMMA')
            param_name = self.expect('NAME').value
            param_type = self.expect('TYPE').value
            params.append(Identifier(param_type, param_name))
        return Parameters("", params)
    
    def parse_expr_statement(self) -> ExprStatement:
        exp = self.parse_expression()
        self.expect('SEMI')
        return ExprStatement(exp)

    def peek(self) -> Token:
        return self.tokens[self.n]

    def peek_k(self, k : int) -> Token: # peeks k tokens ahead
        if self.n + (k - 1) < len(self.tokens):
            return self.tokens[self.n + (k - 1)]
        return Token('EOF', "")

    def parse_statement(self) -> Statement:
        # LL(1):
        next_token = self.peek()
        match next_token.token_type:
            case 'PRINT':
                return self.parse_print()
            case 'IF':
                return self.parse_if()
            case 'WHILE':
                return self.parse_while()
            case 'VAR':
                return self.parse_variable_definition()
            case 'FUNC':
                return self.parse_func()
            case 'RETURN':
                return self.parse_return()
            case 'NAME': # Need to disambiguate between assignment and expression
                if self.peek_k(2).token_type == 'ASSIGN':
                    return self.parse_assignment()
                else:
                    return self.parse_expr_statement()
            case _:
                raise SyntaxError(f'Invalid token for statement: {next_token}')

    def parse_statements(self) -> list[Statement]: # Break out of blocks when we peek a RBRACE token
        statements = []
        while self.peek().token_type != 'RBRACE' and self.peek().token_type != 'EOF':
            statements.append(self.parse_statement())
        return statements
    
    def parse_func_args(self, name) -> FunctionCall:
        self.expect('LPAREN')
        if self.peek().token_type == 'RPAREN': # No arguments
            self.expect('RPAREN')
            return FunctionCall("", name, [])
        
        arguments = [self.parse_expression()] 
        while self.peek().token_type == 'COMMA':
            self.expect('COMMA')
            arguments.append(self.parse_expression())
        self.expect('RPAREN')
        return FunctionCall("", name, arguments)
    

    def parse_term(self) -> Expression:
        next_token = self.peek()
        match next_token.token_type:
            case 'MINUS': # if we are here, it must be a unary op
                self.expect('MINUS')
                return UnaryOp("", '-', self.parse_term())
            case 'INTEGER':
                return Integer(int(self.expect('INTEGER').value))
            case 'FLOAT':
                return Float(float(self.expect('FLOAT').value))
            case 'CHAR':
                return Character(self.expect('CHAR').value)
            case 'NAME': # Either a variable name or function call
                name = Identifier("", self.expect('NAME').value)
                if self.peek().token_type == 'LPAREN':
                    return self.parse_func_args(name)
                else:
                    return name
            case 'LPAREN':
                self.expect('LPAREN')
                inner = self.parse_expression()
                self.expect('RPAREN')
                return inner
            case _:
                raise RuntimeError(f'Expected expression but got {next_token}')

    def parse_expression(self) -> Expression:
        term = self.parse_term()
        peek = self.peek()
        match peek.token_type:
            case 'PLUS' | 'MINUS' | 'TIMES' | 'DIVIDE' | 'LT' | 'LE' | 'GT' | 'GE' | 'EQ' | 'NE':
                self.expect(peek.token_type)
                next_term = self.parse_term()
                return BinaryOp(term.wtype, peek.value, term, next_term)
            case _:
                return term
    
def test_parser():
    tests = ['print 1;',
             'var x = -1;',
             'x = --1;',
             'if 1 == 1 { } else { }',
             'while 1 == 1 { }',
             'func f(x int) int{ }',
             "x = 'c';"
             'return 1;',
             'func f(x int) char{ var x = 1; x = 32;}',
             'func f(x float, y char, z int) int{if 1 == 1 { } else { }}',
             'func f(x int, y int, z int) int{var x = f(0,0,0); x = (2); x = x; x = (x);}',
             'func f(x int) int{var y = ((x) + 10);}',
             'var x = 2 + (3 * (1 + 2));']
    
    for test_program in tests:
        print(Parser(tokenize(test_program)).parse_statement())
        print("")
    '''
    print(Parser(tokenize(tests[0])).parse_print())
    print(Parser(tokenize(tests[1])).parse_variable_definition())
    print(Parser(tokenize(tests[2])).parse_assignment())
    print(Parser(tokenize(tests[3])).parse_if())
    print(Parser(tokenize(tests[4])).parse_while())
    print(Parser(tokenize(tests[5])).parse_func())
    print(Parser(tokenize(tests[6])).parse_return())
    '''

#test_parser()