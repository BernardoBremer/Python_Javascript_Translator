from typing import Dict, List, Optional, Set
from ast_nodes import *

class SemanticError(Exception):
    pass

class Symbol:
    def __init__(self, name: str, symbol_type: str, scope: str):
        self.name = name
        self.type = symbol_type
        self.scope = scope

class SymbolTable:
    def __init__(self):
        self.scopes: List[Dict[str, Symbol]] = [{}]  # Global scope
        self.current_scope = 0
    
    def enter_scope(self):
        self.scopes.append({})
        self.current_scope += 1
    
    def exit_scope(self):
        if self.current_scope > 0:
            self.scopes.pop()
            self.current_scope -= 1
    
    def declare(self, name: str, symbol_type: str):
        scope_name = f"scope_{self.current_scope}"
        symbol = Symbol(name, symbol_type, scope_name)
        self.scopes[self.current_scope][name] = symbol
    
    def lookup(self, name: str) -> Optional[Symbol]:
        for i in range(self.current_scope, -1, -1):
            if name in self.scopes[i]:
                return self.scopes[i][name]
        return None
    
    def is_declared_in_current_scope(self, name: str) -> bool:
        return name in self.scopes[self.current_scope]

class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = SymbolTable()
        self.errors: List[str] = []
        self.current_function = None
        
        # Built-in functions
        self.builtin_functions = {
            'print', 'len', 'range', 'str', 'int', 'float', 'bool', 'list', 'dict'
        }
    
    def analyze(self, ast: Program) -> List[str]:
        self.errors = []
        
        # Declare built-in functions
        for func in self.builtin_functions:
            self.symbol_table.declare(func, 'function')
        
        self.visit_program(ast)
        return self.errors
    
    def error(self, message: str):
        self.errors.append(message)
    
    def visit_program(self, node: Program):
        for stmt in node.statements:
            self.visit_statement(stmt)
    
    def visit_statement(self, node: Statement):
        if isinstance(node, FunctionDef):
            self.visit_function_def(node)
        elif isinstance(node, ClassDef):
            self.visit_class_def(node)
        elif isinstance(node, IfStatement):
            self.visit_if_statement(node)
        elif isinstance(node, ForStatement):
            self.visit_for_statement(node)
        elif isinstance(node, WhileStatement):
            self.visit_while_statement(node)
        elif isinstance(node, ReturnStatement):
            self.visit_return_statement(node)
        elif isinstance(node, AssignStatement):
            self.visit_assign_statement(node)
        elif isinstance(node, ExpressionStatement):
            self.visit_expression(node.expression)
    
    def visit_function_def(self, node: FunctionDef):
        # Check if function already declared in current scope
        if self.symbol_table.is_declared_in_current_scope(node.name):
            self.error(f"Function '{node.name}' already declared in current scope")
        
        # Declare function in current scope
        self.symbol_table.declare(node.name, 'function')
        
        # Enter function scope
        self.symbol_table.enter_scope()
        old_function = self.current_function
        self.current_function = node.name
        
        # Declare parameters
        for param in node.params:
            if self.symbol_table.is_declared_in_current_scope(param):
                self.error(f"Parameter '{param}' already declared")
            self.symbol_table.declare(param, 'variable')
        
        # Visit function body
        for stmt in node.body:
            self.visit_statement(stmt)
        
        # Exit function scope
        self.current_function = old_function
        self.symbol_table.exit_scope()
    
    def visit_class_def(self, node: ClassDef):
        if self.symbol_table.is_declared_in_current_scope(node.name):
            self.error(f"Class '{node.name}' already declared in current scope")
        
        self.symbol_table.declare(node.name, 'class')
        
        # Enter class scope
        self.symbol_table.enter_scope()
        
        for stmt in node.body:
            self.visit_statement(stmt)
        
        self.symbol_table.exit_scope()
    
    def visit_if_statement(self, node: IfStatement):
        self.visit_expression(node.condition)
        
        for stmt in node.then_body:
            self.visit_statement(stmt)
        
        if node.else_body:
            for stmt in node.else_body:
                self.visit_statement(stmt)
    
    def visit_for_statement(self, node: ForStatement):
        self.visit_expression(node.iterable)
        
        # Enter loop scope
        self.symbol_table.enter_scope()
        self.symbol_table.declare(node.target, 'variable')
        
        for stmt in node.body:
            self.visit_statement(stmt)
        
        self.symbol_table.exit_scope()
    
    def visit_while_statement(self, node: WhileStatement):
        self.visit_expression(node.condition)
        
        for stmt in node.body:
            self.visit_statement(stmt)
    
    def visit_return_statement(self, node: ReturnStatement):
        if self.current_function is None:
            self.error("Return statement outside function")
        
        if node.value:
            self.visit_expression(node.value)
    
    def visit_assign_statement(self, node: AssignStatement):
        self.visit_expression(node.value)
        
        # Declare variable if not exists
        if not self.symbol_table.lookup(node.target):
            self.symbol_table.declare(node.target, 'variable')
    
    def visit_expression(self, node: Expression):
        if isinstance(node, BinaryOp):
            self.visit_binary_op(node)
        elif isinstance(node, UnaryOp):
            self.visit_unary_op(node)
        elif isinstance(node, FunctionCall):
            self.visit_function_call(node)
        elif isinstance(node, MethodCall):
            self.visit_method_call(node)
        elif isinstance(node, Identifier):
            self.visit_identifier(node)
        elif isinstance(node, Literal):
            pass  # Literals are always valid
        elif isinstance(node, ListLiteral):
            self.visit_list_literal(node)
        elif isinstance(node, DictLiteral):
            self.visit_dict_literal(node)
        elif isinstance(node, AttributeAccess):
            self.visit_attribute_access(node)
        elif isinstance(node, IndexAccess):
            self.visit_index_access(node)
    
    def visit_binary_op(self, node: BinaryOp):
        self.visit_expression(node.left)
        self.visit_expression(node.right)
        
        # Basic type checking for arithmetic operations
        if node.operator in ['+', '-', '*', '/', '%', '**']:
            # These operations typically work with numbers
            pass
        elif node.operator in ['==', '!=', '<', '<=', '>', '>=']:
            # Comparison operations
            pass
        elif node.operator in ['and', 'or']:
            # Logical operations
            pass
    
    def visit_unary_op(self, node: UnaryOp):
        self.visit_expression(node.operand)
    
    def visit_function_call(self, node: FunctionCall):
        symbol = self.symbol_table.lookup(node.name)
        if not symbol:
            self.error(f"Undefined function '{node.name}'")
        elif symbol.type not in ['function', 'class']:
            self.error(f"'{node.name}' is not a function or class")
        
        for arg in node.args:
            self.visit_expression(arg)
    
    def visit_method_call(self, node):
        self.visit_expression(node.object)
        for arg in node.args:
            self.visit_expression(arg)
    
    def visit_identifier(self, node: Identifier):
        symbol = self.symbol_table.lookup(node.name)
        if not symbol:
            self.error(f"Undefined variable '{node.name}'")
    
    def visit_list_literal(self, node: ListLiteral):
        for element in node.elements:
            self.visit_expression(element)
    
    def visit_dict_literal(self, node: DictLiteral):
        for key, value in node.pairs:
            self.visit_expression(key)
            self.visit_expression(value)
    
    def visit_attribute_access(self, node: AttributeAccess):
        self.visit_expression(node.object)
    
    def visit_index_access(self, node: IndexAccess):
        self.visit_expression(node.object)
        self.visit_expression(node.index)
