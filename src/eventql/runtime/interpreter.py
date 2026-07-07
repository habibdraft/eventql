import torch
from eventql.ast.nodes import Signal, Constant, Diff, Shift, Cumsum, Eq, Lt, Gt, And, Or, Enter, Exit, Before, After, Between

def expand_events(node, events):

    # --------------------
    # base cases
    # --------------------
    if isinstance(node, Signal):
        if node.name in events:
            return expand_events(events[node.name], events)
        return node

    if isinstance(node, Constant):
        return node

    # --------------------
    # unary ops
    # --------------------
    if hasattr(node, "expr"):
        return type(node)(
            expand_events(node.expr, events)
        )

    # --------------------
    # binary ops
    # --------------------
    if hasattr(node, "left") and hasattr(node, "right"):
        return type(node)(
            expand_events(node.left, events),
            expand_events(node.right, events)
        )

    # --------------------
    # fallback
    # --------------------
    return node

def eval_value(node, ctx):

    # -----------------------
    # base signals
    # -----------------------
    if isinstance(node, Signal):
        return ctx[node.name]

    if isinstance(node, Constant):
        return torch.tensor(node.value)

    # -----------------------
    # temporal primitives
    # -----------------------

    if isinstance(node, Shift):
        x = eval_value(node.expr, ctx)
        k = int(node.k)

        if x.dtype == torch.bool:
            ret = torch.zeros_like(x)
        else:
            ret = torch.full_like(x, float('nan'))

        if k == 0:
            return x.clone()

        if k > 0:
            ret[k:] = x[:-k]
            return ret

        if k < 0:
            ret[:k] = x[-k:]
            return ret

    if isinstance(node, Diff):
        x = eval_value(node.expr, ctx)
        x_prev = eval_value(Shift(node.expr, 1), ctx)
        return x - x_prev

    if isinstance(node, Cumsum):
        x = eval_value(node.expr, ctx)
        return torch.cumsum(x, dim=0)

    # -----------------------
    # comparisons
    # -----------------------

    if isinstance(node, Eq):
        return eval_value(node.left, ctx) == eval_value(node.right, ctx)

    if isinstance(node, Lt):
        return eval_value(node.left, ctx) < eval_value(node.right, ctx)

    if isinstance(node, Gt):
        return eval_value(node.left, ctx) > eval_value(node.right, ctx)

    # -----------------------
    # boolean ops
    # -----------------------

    if isinstance(node, And):
        return eval_value(node.left, ctx) & eval_value(node.right, ctx)

    if isinstance(node, Or):
        return eval_value(node.left, ctx) | eval_value(node.right, ctx)

    # -----------------------
    # flags
    # -----------------------

    if isinstance(node, Enter):
        x = eval_value(node.expr, ctx)
        x_prev = eval_value(Shift(node.expr, 1), ctx)
        return x & ~x_prev

    if isinstance(node, Exit):
        x = eval_value(node.expr, ctx)
        x_prev = eval_value(Shift(node.expr, 1), ctx)
        return ~x & x_prev

    if isinstance(node, Before):
        x = eval_value(node.expr, ctx)
        c = torch.cumsum(x, dim=0)
        return c < 1

    if isinstance(node, After):
        x = eval_value(node.expr, ctx)
        c = torch.cumsum(x, dim=0)
        return c >= 1

    if isinstance(node, Between):
        left = eval_value(node.left, ctx)
        right = eval_value(node.right, ctx)

        return(
            torch.cumsum(left.int(), dim=0)
            >
            torch.cumsum(right.int(), dim=0)
        )
