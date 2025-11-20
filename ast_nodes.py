from abc import ABC, abstractmethod
from typing import List, Optional, Any
from dataclasses import dataclass

class ASTNode(ABC):
    pass

class Statement(ASTNode):
    pass

class Expression(ASTNode):
    pass

@dataclass
class Program(ASTNode):
    statements: List[Statement]

@dataclass
class FunctionDef(Statement):
    name: str
    params: List[str]
    body: List[Statement]

@dataclass
class ClassDef(Statement):
    name: str
    body: List[Statement]

@dataclass
class IfStatement(Statement):
    condition: Expression
    then_body: List[Statement]
    else_body: Optional[List[Statement]] = None

@dataclass
class ForStatement(Statement):
    target: str
    iterable: Expression
    body: List[Statement]

@dataclass
class WhileStatement(Statement):
    condition: Expression
    body: List[Statement]

@dataclass
class ReturnStatement(Statement):
    value: Optional[Expression] = None

@dataclass
class AssignStatement(Statement):
    target: str
    value: Expression

@dataclass
class ExpressionStatement(Statement):
    expression: Expression

@dataclass
class BinaryOp(Expression):
    left: Expression
    operator: str
    right: Expression

@dataclass
class UnaryOp(Expression):
    operator: str
    operand: Expression

@dataclass
class FunctionCall(Expression):
    name: str
    args: List[Expression]

@dataclass
class MethodCall(Expression):
    object: Expression
    method: str
    args: List[Expression]

@dataclass
class Identifier(Expression):
    name: str

@dataclass
class Literal(Expression):
    value: Any
    type: str  # 'number', 'string', 'boolean', 'none'

@dataclass
class ListLiteral(Expression):
    elements: List[Expression]

@dataclass
class DictLiteral(Expression):
    pairs: List[tuple[Expression, Expression]]

@dataclass
class AttributeAccess(Expression):
    object: Expression
    attribute: str

@dataclass
class IndexAccess(Expression):
    object: Expression
    index: Expression
