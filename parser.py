from typing import List, Optional
from lexer import Token, TokenType, Lexer
from ast_nodes import *

class ParseError(Exception):
    pass

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0
    
    def current_token(self) -> Token:
        return self.tokens[self.pos] if self.pos < len(self.tokens) else self.tokens[-1]
    
    def peek_token(self, offset: int = 1) -> Token:
        peek_pos = self.pos + offset
        return self.tokens[peek_pos] if peek_pos < len(self.tokens) else self.tokens[-1]
    
    def advance(self):
        if self.pos < len(self.tokens) - 1:
            self.pos += 1
    
    def match(self, token_type: TokenType) -> bool:
        return self.current_token().type == token_type
    
    def consume(self, token_type: TokenType) -> Token:
        if not self.match(token_type):
            raise ParseError(f"Expected {token_type}, got {self.current_token().type}")
        token = self.current_token()
        self.advance()
        return token
    
    def skip_newlines(self):
        while self.match(TokenType.NEWLINE):
            self.advance()
    
    def parse(self) -> Program:
        statements = []
        self.skip_newlines()
        
        while not self.match(TokenType.EOF):
            if self.match(TokenType.NEWLINE):
                self.advance()
                continue
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
        
        return Program(statements)
    
    def parse_statement(self) -> Optional[Statement]:
        self.skip_newlines()
        
        if self.match(TokenType.DEF):
            return self.parse_function_def()
        elif self.match(TokenType.CLASS):
            return self.parse_class_def()
        elif self.match(TokenType.IF):
            return self.parse_if_statement()
        elif self.match(TokenType.FOR):
            return self.parse_for_statement()
        elif self.match(TokenType.WHILE):
            return self.parse_while_statement()
        elif self.match(TokenType.RETURN):
            return self.parse_return_statement()
        elif self.match(TokenType.IDENTIFIER) and self.peek_token().type == TokenType.ASSIGN:
            return self.parse_assignment()
        else:
            expr = self.parse_expression()
            if expr:
                return ExpressionStatement(expr)
        
        return None
    
    def parse_function_def(self) -> FunctionDef:
        self.consume(TokenType.DEF)
        name = self.consume(TokenType.IDENTIFIER).value
        self.consume(TokenType.LPAREN)
        
        params = []
        while not self.match(TokenType.RPAREN):
            params.append(self.consume(TokenType.IDENTIFIER).value)
            if self.match(TokenType.COMMA):
                self.advance()
        
        self.consume(TokenType.RPAREN)
        self.consume(TokenType.COLON)
        body = self.parse_block()
        
        return FunctionDef(name, params, body)
    
    def parse_class_def(self) -> ClassDef:
        self.consume(TokenType.CLASS)
        name = self.consume(TokenType.IDENTIFIER).value
        self.consume(TokenType.COLON)
        
        # Enter class scope and parse methods
        self.skip_newlines()
        if not self.match(TokenType.INDENT):
            # Empty class body
            return ClassDef(name, [])
        
        self.consume(TokenType.INDENT)
        body = []
        
        while not self.match(TokenType.DEDENT) and not self.match(TokenType.EOF):
            if self.match(TokenType.NEWLINE):
                self.advance()
                continue
            
            # Parse class methods (only def statements allowed in class)
            if self.match(TokenType.DEF):
                method = self.parse_function_def()
                body.append(method)
            else:
                # Skip other statements for now
                self.advance()
        
        if self.match(TokenType.DEDENT):
            self.advance()
        
        return ClassDef(name, body)
    
    def parse_if_statement(self) -> IfStatement:
        self.consume(TokenType.IF)
        condition = self.parse_expression()
        self.consume(TokenType.COLON)
        then_body = self.parse_block()
        
        else_body = None
        if self.match(TokenType.ELIF):
            # Treat elif as nested if-else
            elif_stmt = self.parse_elif_chain()
            else_body = [elif_stmt]
        elif self.match(TokenType.ELSE):
            self.advance()
            self.consume(TokenType.COLON)
            else_body = self.parse_block()
        
        return IfStatement(condition, then_body, else_body)
    
    def parse_elif_chain(self) -> IfStatement:
        """Parse elif as a nested if statement"""
        self.consume(TokenType.ELIF)
        condition = self.parse_expression()
        self.consume(TokenType.COLON)
        then_body = self.parse_block()
        
        else_body = None
        if self.match(TokenType.ELIF):
            # Another elif - recurse
            elif_stmt = self.parse_elif_chain()
            else_body = [elif_stmt]
        elif self.match(TokenType.ELSE):
            self.advance()
            self.consume(TokenType.COLON)
            else_body = self.parse_block()
        
        return IfStatement(condition, then_body, else_body)
    
    def parse_for_statement(self) -> ForStatement:
        self.consume(TokenType.FOR)
        target = self.consume(TokenType.IDENTIFIER).value
        self.consume(TokenType.IN)
        iterable = self.parse_expression()
        self.consume(TokenType.COLON)
        body = self.parse_block()
        
        return ForStatement(target, iterable, body)
    
    def parse_while_statement(self) -> WhileStatement:
        self.consume(TokenType.WHILE)
        condition = self.parse_expression()
        self.consume(TokenType.COLON)
        body = self.parse_block()
        
        return WhileStatement(condition, body)
    
    def parse_return_statement(self) -> ReturnStatement:
        self.consume(TokenType.RETURN)
        value = None
        if not self.match(TokenType.NEWLINE) and not self.match(TokenType.EOF):
            value = self.parse_expression()
        return ReturnStatement(value)
    
    def parse_assignment(self) -> AssignStatement:
        target = self.consume(TokenType.IDENTIFIER).value
        self.consume(TokenType.ASSIGN)
        value = self.parse_expression()
        return AssignStatement(target, value)
    
    def parse_block(self) -> List[Statement]:
        statements = []
        self.skip_newlines()
        
        if not self.match(TokenType.INDENT):
            # Single statement on same line (not typical Python but handle it)
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
            return statements
        
        self.consume(TokenType.INDENT)
        
        while not self.match(TokenType.DEDENT) and not self.match(TokenType.EOF):
            if self.match(TokenType.NEWLINE):
                self.advance()
                continue
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
        
        if self.match(TokenType.DEDENT):
            self.advance()
        
        return statements
    
    def parse_expression(self) -> Expression:
        return self.parse_or_expression()
    
    def parse_or_expression(self) -> Expression:
        left = self.parse_and_expression()
        
        while self.match(TokenType.OR):
            op = self.current_token().value
            self.advance()
            right = self.parse_and_expression()
            left = BinaryOp(left, op, right)
        
        return left
    
    def parse_and_expression(self) -> Expression:
        left = self.parse_equality_expression()
        
        while self.match(TokenType.AND):
            op = self.current_token().value
            self.advance()
            right = self.parse_equality_expression()
            left = BinaryOp(left, op, right)
        
        return left
    
    def parse_equality_expression(self) -> Expression:
        left = self.parse_comparison_expression()
        
        while self.match(TokenType.EQ) or self.match(TokenType.NE):
            op = self.current_token().value
            self.advance()
            right = self.parse_comparison_expression()
            left = BinaryOp(left, op, right)
        
        return left
    
    def parse_comparison_expression(self) -> Expression:
        left = self.parse_additive_expression()
        
        while (self.match(TokenType.LT) or self.match(TokenType.LE) or 
               self.match(TokenType.GT) or self.match(TokenType.GE)):
            op = self.current_token().value
            self.advance()
            right = self.parse_additive_expression()
            left = BinaryOp(left, op, right)
        
        return left
    
    def parse_additive_expression(self) -> Expression:
        left = self.parse_multiplicative_expression()
        
        while self.match(TokenType.PLUS) or self.match(TokenType.MINUS):
            op = self.current_token().value
            self.advance()
            right = self.parse_multiplicative_expression()
            left = BinaryOp(left, op, right)
        
        return left
    
    def parse_multiplicative_expression(self) -> Expression:
        left = self.parse_power_expression()
        
        while (self.match(TokenType.MULTIPLY) or self.match(TokenType.DIVIDE) or 
               self.match(TokenType.MODULO)):
            op = self.current_token().value
            self.advance()
            right = self.parse_power_expression()
            left = BinaryOp(left, op, right)
        
        return left
    
    def parse_power_expression(self) -> Expression:
        left = self.parse_unary_expression()
        
        if self.match(TokenType.POWER):
            op = self.current_token().value
            self.advance()
            right = self.parse_power_expression()  # Right associative
            left = BinaryOp(left, op, right)
        
        return left
    
    def parse_unary_expression(self) -> Expression:
        if self.match(TokenType.NOT) or self.match(TokenType.MINUS):
            op = self.current_token().value
            self.advance()
            operand = self.parse_unary_expression()
            return UnaryOp(op, operand)
        
        return self.parse_postfix_expression()
    
    def parse_postfix_expression(self) -> Expression:
        expr = self.parse_primary_expression()
        
        while True:
            if self.match(TokenType.LPAREN):
                # Function call
                self.advance()
                args = []
                while not self.match(TokenType.RPAREN):
                    args.append(self.parse_expression())
                    if self.match(TokenType.COMMA):
                        self.advance()
                self.consume(TokenType.RPAREN)
                
                if isinstance(expr, Identifier):
                    expr = FunctionCall(expr.name, args)
                elif isinstance(expr, AttributeAccess):
                    # Method call
                    expr = MethodCall(expr.object, expr.attribute, args)
                else:
                    raise ParseError("Invalid function call")
            
            elif self.match(TokenType.DOT):
                # Attribute access
                self.advance()
                attr = self.consume(TokenType.IDENTIFIER).value
                expr = AttributeAccess(expr, attr)
            
            elif self.match(TokenType.LBRACKET):
                # Index access
                self.advance()
                index = self.parse_expression()
                self.consume(TokenType.RBRACKET)
                expr = IndexAccess(expr, index)
            
            else:
                break
        
        return expr
    
    def parse_primary_expression(self) -> Expression:
        if self.match(TokenType.NUMBER):
            value = self.current_token().value
            self.advance()
            return Literal(float(value) if '.' in value else int(value), 'number')
        
        elif self.match(TokenType.STRING):
            value = self.current_token().value
            self.advance()
            return Literal(value, 'string')
        
        elif self.match(TokenType.TRUE):
            self.advance()
            return Literal(True, 'boolean')
        
        elif self.match(TokenType.FALSE):
            self.advance()
            return Literal(False, 'boolean')
        
        elif self.match(TokenType.NONE):
            self.advance()
            return Literal(None, 'none')
        
        elif self.match(TokenType.IDENTIFIER):
            name = self.current_token().value
            self.advance()
            return Identifier(name)
        
        elif self.match(TokenType.LBRACKET):
            return self.parse_list_literal()
        
        elif self.match(TokenType.LBRACE):
            return self.parse_dict_literal()
        
        elif self.match(TokenType.LPAREN):
            self.advance()
            expr = self.parse_expression()
            self.consume(TokenType.RPAREN)
            return expr
        
        else:
            raise ParseError(f"Unexpected token: {self.current_token().type}")
    
    def parse_list_literal(self) -> ListLiteral:
        self.consume(TokenType.LBRACKET)
        elements = []
        
        while not self.match(TokenType.RBRACKET):
            elements.append(self.parse_expression())
            if self.match(TokenType.COMMA):
                self.advance()
        
        self.consume(TokenType.RBRACKET)
        return ListLiteral(elements)
    
    def parse_dict_literal(self) -> DictLiteral:
        self.consume(TokenType.LBRACE)
        pairs = []
        
        while not self.match(TokenType.RBRACE):
            key = self.parse_expression()
            self.consume(TokenType.COLON)
            value = self.parse_expression()
            pairs.append((key, value))
            
            if self.match(TokenType.COMMA):
                self.advance()
        
        self.consume(TokenType.RBRACE)
        return DictLiteral(pairs)
