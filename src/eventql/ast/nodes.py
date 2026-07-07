# nodes.py

from dataclasses import dataclass

class Node:
    pass

@dataclass
class Signal(Node):
    name: str

@dataclass
class Constant(Node):
    value: float

@dataclass
class Diff(Node):
    expr: Node

@dataclass
class Shift(Node):
    expr: Node
    k: int

@dataclass
class Enter(Node):
    expr: Node

@dataclass
class Exit(Node):
    expr: Node

@dataclass
class Before(Node):
    expr: Node

@dataclass
class After(Node):
    expr: Node

@dataclass
class Cumsum(Node):
    expr: Node

@dataclass
class Eq(Node):
    left: Node
    right: Node


@dataclass
class Lt(Node):
    left: Node
    right: Node


@dataclass
class Gt(Node):
    left: Node
    right: Node


@dataclass
class And(Node):
    left: Node
    right: Node


@dataclass
class Or(Node):
    left: Node
    right: Node

@dataclass
class Between(Node):
    left: Node
    right: Node
