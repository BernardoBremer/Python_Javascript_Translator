from typing import List
from ast_nodes import *

class CodeGenerator:
    def __init__(self):
        self.indent_level = 0
        self.output = []
    
    def indent(self) -> str:
        return "  " * self.indent_level
    
    def generate(self, ast: Program) -> str:
        self.output = []
        self.visit_program(ast)
        return "\n".join(self.output)
    
    def emit(self, code: str):
        self.output.append(self.indent() + code)
    
    def visit_program(self, node: Program):
        for stmt in node.statements:
            self.visit_statement(stmt)
            # Add empty line after function definitions
            if isinstance(stmt, FunctionDef):
                self.emit("")
    
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
            self.visit_expression_statement(node)
    
    def visit_function_def(self, node: FunctionDef):
        params = ", ".join(node.params)
        self.emit(f"function {node.name}({params}) {{")
        self.indent_level += 1
        
        for stmt in node.body:
            self.visit_statement(stmt)
        
        self.indent_level -= 1
        self.emit("}")
    
    def visit_class_def(self, node: ClassDef):
        self.emit(f"class {node.name} {{")
        self.indent_level += 1
        
        for stmt in node.body:
            if isinstance(stmt, FunctionDef):
                # Generate method without 'function' keyword
                params = ", ".join(stmt.params)
                self.emit(f"{stmt.name}({params}) {{")
                self.indent_level += 1
                
                for method_stmt in stmt.body:
                    self.visit_statement(method_stmt)
                
                self.indent_level -= 1
                self.emit("}")
            else:
                self.visit_statement(stmt)
        
        self.indent_level -= 1
        self.emit("}")
    
    def visit_if_statement(self, node: IfStatement):
        condition = self.visit_expression(node.condition)
        self.emit(f"if ({condition}) {{")
        self.indent_level += 1
        
        for stmt in node.then_body:
            self.visit_statement(stmt)
        
        self.indent_level -= 1
        
        if node.else_body:
            self.emit("} else {")
            self.indent_level += 1
            
            for stmt in node.else_body:
                self.visit_statement(stmt)
            
            self.indent_level -= 1
        
        self.emit("}")
    
    def visit_for_statement(self, node: ForStatement):
        iterable = self.visit_expression(node.iterable)
        self.emit(f"for (const {node.target} of {iterable}) {{")
        self.indent_level += 1
        
        for stmt in node.body:
            self.visit_statement(stmt)
        
        self.indent_level -= 1
        self.emit("}")
    
    def visit_while_statement(self, node: WhileStatement):
        condition = self.visit_expression(node.condition)
        self.emit(f"while ({condition}) {{")
        self.indent_level += 1
        
        for stmt in node.body:
            self.visit_statement(stmt)
        
        self.indent_level -= 1
        self.emit("}")
    
    def visit_return_statement(self, node: ReturnStatement):
        if node.value:
            value = self.visit_expression(node.value)
            self.emit(f"return {value};")
        else:
            self.emit("return;")
    
    def visit_assign_statement(self, node: AssignStatement):
        value = self.visit_expression(node.value)
        self.emit(f"let {node.target} = {value};")
    
    def visit_expression_statement(self, node: ExpressionStatement):
        expr = self.visit_expression(node.expression)
        self.emit(f"{expr};")
    
    def visit_expression(self, node: Expression) -> str:
        if isinstance(node, BinaryOp):
            return self.visit_binary_op(node)
        elif isinstance(node, UnaryOp):
            return self.visit_unary_op(node)
        elif isinstance(node, FunctionCall):
            return self.visit_function_call(node)
        elif isinstance(node, MethodCall):
            return self.visit_method_call(node)
        elif isinstance(node, Identifier):
            return self.visit_identifier(node)
        elif isinstance(node, Literal):
            return self.visit_literal(node)
        elif isinstance(node, ListLiteral):
            return self.visit_list_literal(node)
        elif isinstance(node, DictLiteral):
            return self.visit_dict_literal(node)
        elif isinstance(node, AttributeAccess):
            return self.visit_attribute_access(node)
        elif isinstance(node, IndexAccess):
            return self.visit_index_access(node)
        else:
            return "undefined"
    
    def visit_binary_op(self, node: BinaryOp) -> str:
        left = self.visit_expression(node.left)
        right = self.visit_expression(node.right)
        
        # Map Python operators to JavaScript
        operator_map = {
            'and': '&&',
            'or': '||',
            '**': '**',
            '//': 'Math.floor',  # Special case for floor division
        }
        
        op = operator_map.get(node.operator, node.operator)
        
        if node.operator == '//':
            return f"Math.floor({left} / {right})"
        else:
            return f"({left} {op} {right})"
    
    def visit_unary_op(self, node: UnaryOp) -> str:
        operand = self.visit_expression(node.operand)
        
        operator_map = {
            'not': '!',
            '-': '-',
            '+': '+'
        }
        
        op = operator_map.get(node.operator, node.operator)
        return f"{op}{operand}"
    
    def visit_function_call(self, node: FunctionCall) -> str:
        args = [self.visit_expression(arg) for arg in node.args]
        args_str = ", ".join(args)
        
        # Map Python built-in functions to JavaScript
        builtin_map = {
            'print': 'console.log',
            'len': lambda args: f"{args[0]}.length" if args else "0",
            'str': 'String',
            'int': 'parseInt',
            'float': 'parseFloat',
            'bool': 'Boolean',
            'list': lambda args: f"[{', '.join(args)}]" if args else "[]",
            'dict': lambda args: "{}" if not args else f"{{{args[0]}}}",
            'range': self.generate_range_function
        }
        
        if node.name in builtin_map:
            mapping = builtin_map[node.name]
            if callable(mapping):
                return mapping(args)
            else:
                return f"{mapping}({args_str})"
        else:
            # Check if it's a class constructor (starts with uppercase)
            if node.name[0].isupper():
                return f"new {node.name}({args_str})"
            else:
                return f"{node.name}({args_str})"
    
    def generate_range_function(self, args: List[str]) -> str:
        if len(args) == 1:
            return f"Array.from({{length: {args[0]}}}, (_, i) => i)"
        elif len(args) == 2:
            return f"Array.from({{length: {args[1]} - {args[0]}}}, (_, i) => i + {args[0]})"
        elif len(args) == 3:
            start, stop, step = args
            return f"Array.from({{length: Math.ceil(({stop} - {start}) / {step})}}, (_, i) => {start} + i * {step})"
        else:
            return "[]"
    
    def visit_method_call(self, node) -> str:
        obj = self.visit_expression(node.object)
        args = [self.visit_expression(arg) for arg in node.args]
        args_str = ", ".join(args)
        return f"{obj}.{node.method}({args_str})"
    
    def visit_identifier(self, node: Identifier) -> str:
        return node.name
    
    def visit_literal(self, node: Literal) -> str:
        if node.type == 'string':
            return f'"{node.value}"'
        elif node.type == 'number':
            return str(node.value)
        elif node.type == 'boolean':
            return 'true' if node.value else 'false'
        elif node.type == 'none':
            return 'null'
        else:
            return str(node.value)
    
    def visit_list_literal(self, node: ListLiteral) -> str:
        elements = [self.visit_expression(elem) for elem in node.elements]
        return f"[{', '.join(elements)}]"
    
    def visit_dict_literal(self, node: DictLiteral) -> str:
        pairs = []
        for key, value in node.pairs:
            key_str = self.visit_expression(key)
            value_str = self.visit_expression(value)
            pairs.append(f"{key_str}: {value_str}")
        return f"{{{', '.join(pairs)}}}"
    
    def visit_attribute_access(self, node: AttributeAccess) -> str:
        obj = self.visit_expression(node.object)
        return f"{obj}.{node.attribute}"
    
    def visit_index_access(self, node: IndexAccess) -> str:
        obj = self.visit_expression(node.object)
        index = self.visit_expression(node.index)
        return f"{obj}[{index}]"
