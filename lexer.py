import re
from enum import Enum
from dataclasses import dataclass
from typing import List, Optional

class TokenType(Enum):
    # Literals
    NUMBER = "NUMBER"
    STRING = "STRING"
    IDENTIFIER = "IDENTIFIER"
    
    # Keywords
    DEF = "def"
    IF = "if"
    ELSE = "else"
    ELIF = "elif"
    FOR = "for"
    WHILE = "while"
    RETURN = "return"
    CLASS = "class"
    IMPORT = "import"
    FROM = "from"
    AS = "as"
    TRUE = "True"
    FALSE = "False"
    NONE = "None"
    AND = "and"
    OR = "or"
    NOT = "not"
    IN = "in"
    IS = "is"
    
    # Operators
    PLUS = "+"
    MINUS = "-"
    MULTIPLY = "*"
    DIVIDE = "/"
    MODULO = "%"
    POWER = "**"
    ASSIGN = "="
    PLUS_ASSIGN = "+="
    MINUS_ASSIGN = "-="
    EQ = "=="
    NE = "!="
    LT = "<"
    LE = "<="
    GT = ">"
    GE = ">="
    
    # Delimiters
    LPAREN = "("
    RPAREN = ")"
    LBRACKET = "["
    RBRACKET = "]"
    LBRACE = "{"
    RBRACE = "}"
    COMMA = ","
    COLON = ":"
    DOT = "."
    
    # Special
    NEWLINE = "NEWLINE"
    INDENT = "INDENT"
    DEDENT = "DEDENT"
    EOF = "EOF"

@dataclass
class Token:
    type: TokenType
    value: str
    line: int
    column: int

class Lexer:
    def __init__(self, text: str):
        self.text = text
        self.pos = 0
        self.line = 1
        self.column = 1
        self.indent_stack = [0]
        
        self.keywords = {
            'def', 'if', 'else', 'elif', 'for', 'while', 'return', 'class',
            'import', 'from', 'as', 'True', 'False', 'None', 'and', 'or',
            'not', 'in', 'is'
        }
        
    def current_char(self) -> Optional[str]:
        return self.text[self.pos] if self.pos < len(self.text) else None
    
    def peek_char(self, offset: int = 1) -> Optional[str]:
        peek_pos = self.pos + offset
        return self.text[peek_pos] if peek_pos < len(self.text) else None
    
    def advance(self):
        if self.pos < len(self.text) and self.text[self.pos] == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        self.pos += 1
    
    def skip_whitespace(self):
        while self.current_char() and self.current_char() in ' \t':
            self.advance()
    
    def read_number(self) -> Token:
        start_pos = self.pos
        start_col = self.column
        
        while self.current_char() and (self.current_char().isdigit() or self.current_char() == '.'):
            self.advance()
        
        value = self.text[start_pos:self.pos]
        return Token(TokenType.NUMBER, value, self.line, start_col)
    
    def read_string(self) -> Token:
        quote_char = self.current_char()
        start_col = self.column
        self.advance()  # Skip opening quote
        
        value = ""
        while self.current_char() and self.current_char() != quote_char:
            if self.current_char() == '\\':
                self.advance()
                if self.current_char():
                    value += self.current_char()
                    self.advance()
            else:
                value += self.current_char()
                self.advance()
        
        if self.current_char() == quote_char:
            self.advance()  # Skip closing quote
        
        return Token(TokenType.STRING, value, self.line, start_col)
    
    def read_identifier(self) -> Token:
        start_pos = self.pos
        start_col = self.column
        
        while (self.current_char() and 
               (self.current_char().isalnum() or self.current_char() == '_')):
            self.advance()
        
        value = self.text[start_pos:self.pos]
        token_type = TokenType.IDENTIFIER
        
        if value in self.keywords:
            token_type = TokenType(value)
        
        return Token(token_type, value, self.line, start_col)
    
    def handle_indentation(self) -> List[Token]:
        tokens = []
        indent_level = 0
        
        while self.current_char() and self.current_char() in ' \t':
            if self.current_char() == ' ':
                indent_level += 1
            else:  # tab
                indent_level += 4
            self.advance()
        
        # Skip empty lines and comments
        if self.current_char() == '\n' or self.current_char() == '#' or self.current_char() is None:
            return tokens
        
        current_indent = self.indent_stack[-1]
        
        if indent_level > current_indent:
            self.indent_stack.append(indent_level)
            tokens.append(Token(TokenType.INDENT, "", self.line, self.column))
        elif indent_level < current_indent:
            while self.indent_stack and self.indent_stack[-1] > indent_level:
                self.indent_stack.pop()
                tokens.append(Token(TokenType.DEDENT, "", self.line, self.column))
        
        return tokens
    
    def tokenize(self) -> List[Token]:
        tokens = []
        at_line_start = True
        
        while self.pos < len(self.text):
            char = self.current_char()
            
            if at_line_start:
                if char in ' \t':
                    indent_tokens = self.handle_indentation()
                    tokens.extend(indent_tokens)
                    at_line_start = False
                    continue
                elif char == '\n':
                    # Empty line - check if we need to generate DEDENT
                    if len(self.indent_stack) > 1:
                        # Generate DEDENT for empty line at base indentation
                        while len(self.indent_stack) > 1:
                            self.indent_stack.pop()
                            tokens.append(Token(TokenType.DEDENT, "", self.line, self.column))
                    tokens.append(Token(TokenType.NEWLINE, char, self.line, self.column))
                    self.advance()
                    continue
                else:
                    # Non-whitespace at start of line with no indentation
                    if len(self.indent_stack) > 1:
                        while len(self.indent_stack) > 1:
                            self.indent_stack.pop()
                            tokens.append(Token(TokenType.DEDENT, "", self.line, self.column))
                    at_line_start = False
            
            if char == '\n':
                tokens.append(Token(TokenType.NEWLINE, char, self.line, self.column))
                self.advance()
                at_line_start = True
                continue
            
            if char in ' \t':
                self.skip_whitespace()
            elif char == '#':
                while self.current_char() and self.current_char() != '\n':
                    self.advance()
            elif char.isdigit():
                tokens.append(self.read_number())
            elif char in '"\'':
                tokens.append(self.read_string())
            elif char.isalpha() or char == '_':
                tokens.append(self.read_identifier())
            elif char == '+':
                if self.peek_char() == '=':
                    tokens.append(Token(TokenType.PLUS_ASSIGN, "+=", self.line, self.column))
                    self.advance()
                    self.advance()
                else:
                    tokens.append(Token(TokenType.PLUS, char, self.line, self.column))
                    self.advance()
            elif char == '-':
                if self.peek_char() == '=':
                    tokens.append(Token(TokenType.MINUS_ASSIGN, "-=", self.line, self.column))
                    self.advance()
                    self.advance()
                else:
                    tokens.append(Token(TokenType.MINUS, char, self.line, self.column))
                    self.advance()
            elif char == '*':
                if self.peek_char() == '*':
                    tokens.append(Token(TokenType.POWER, "**", self.line, self.column))
                    self.advance()
                    self.advance()
                else:
                    tokens.append(Token(TokenType.MULTIPLY, char, self.line, self.column))
                    self.advance()
            elif char == '=':
                if self.peek_char() == '=':
                    tokens.append(Token(TokenType.EQ, "==", self.line, self.column))
                    self.advance()
                    self.advance()
                else:
                    tokens.append(Token(TokenType.ASSIGN, char, self.line, self.column))
                    self.advance()
            elif char == '!':
                if self.peek_char() == '=':
                    tokens.append(Token(TokenType.NE, "!=", self.line, self.column))
                    self.advance()
                    self.advance()
            elif char == '<':
                if self.peek_char() == '=':
                    tokens.append(Token(TokenType.LE, "<=", self.line, self.column))
                    self.advance()
                    self.advance()
                else:
                    tokens.append(Token(TokenType.LT, char, self.line, self.column))
                    self.advance()
            elif char == '>':
                if self.peek_char() == '=':
                    tokens.append(Token(TokenType.GE, ">=", self.line, self.column))
                    self.advance()
                    self.advance()
                else:
                    tokens.append(Token(TokenType.GT, char, self.line, self.column))
                    self.advance()
            else:
                # Single character tokens
                token_map = {
                    '/': TokenType.DIVIDE, '%': TokenType.MODULO,
                    '(': TokenType.LPAREN, ')': TokenType.RPAREN,
                    '[': TokenType.LBRACKET, ']': TokenType.RBRACKET,
                    '{': TokenType.LBRACE, '}': TokenType.RBRACE,
                    ',': TokenType.COMMA, ':': TokenType.COLON,
                    '.': TokenType.DOT
                }
                
                if char in token_map:
                    tokens.append(Token(token_map[char], char, self.line, self.column))
                
                self.advance()
        
        # Add final DEDENT tokens for remaining indentation levels
        while len(self.indent_stack) > 1:
            self.indent_stack.pop()
            tokens.append(Token(TokenType.DEDENT, "", self.line, self.column))
        
        tokens.append(Token(TokenType.EOF, "", self.line, self.column))
        return tokens
