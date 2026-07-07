# infer_type.py

from eventql.semantics.types import DSLType
from eventql.ast.nodes import Signal, Constant, Diff, Shift, Cumsum, Eq, Lt, Gt, And, Or, Enter, Exit, Before, After, Between

def infer_type(node):

    if isinstance(node, Signal):
        return DSLType.SIGNAL

    if isinstance(node, Constant):
        return DSLType.SCALAR

    if isinstance(node, Diff):
        return DSLType.SIGNAL

    if isinstance(node, Shift):
        return infer_type(node.expr)

    if isinstance(node, Cumsum):
        return DSLType.SIGNAL

    if isinstance(node, Eq):
        lt = infer_type(node.left)
        rt = infer_type(node.right)

        if lt == DSLType.SCALAR and rt == DSLType.SCALAR:
            return DSLType.SCALAR

        return DSLType.MASK

    if isinstance(node, Lt):
        lt = infer_type(node.left)
        rt = infer_type(node.right)

        if lt == DSLType.SCALAR and rt == DSLType.SCALAR:
            return DSLType.SCALAR

        return DSLType.MASK

    if isinstance(node, Gt):
        lt = infer_type(node.left)
        rt = infer_type(node.right)

        if lt == DSLType.SCALAR and rt == DSLType.SCALAR:
            return DSLType.SCALAR

        return DSLType.MASK

    if isinstance(node, And):
        return DSLType.MASK

    if isinstance(node, Or):
        return DSLType.MASK

    if isinstance(node, Enter):
        return DSLType.MASK

    if isinstance(node, Exit):
        return DSLType.MASK

    if isinstance(node, Before):
        return DSLType.MASK

    if isinstance(node, After):
        return DSLType.MASK

    if isinstance(node, Between):
        return DSLType.MASK

    raise Exception(f"Unknown node: {node}")
