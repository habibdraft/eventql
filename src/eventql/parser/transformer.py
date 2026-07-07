# transformer.py

from lark import Transformer
from eventql.ast.nodes import Signal, Constant, Diff, Shift, Cumsum, Eq, Lt, Gt, And, Or, Enter, Exit, Before, After, Between


class ASTBuilder(Transformer):

    def NAME(self, token):
        return Signal(token.value)

    def SIGNED_NUMBER(self, token):
        return Constant(float(token.value))

    def diff(self, items):
        return Diff(items[0])

    def shift(self, items):
        expr = items[0]
        k = items[1]
        return Shift(expr, int(k.value))

    def cumsum(self, items):
        return Cumsum(items[0])

    def eq(self, items):
        return Eq(items[0], items[1])

    def lt(self, items):
        return Lt(items[0], items[1])

    def gt(self, items):
        return Gt(items[0], items[1])

    def and_expr(self, items):
        return And(items[0], items[1])

    def or_expr(self, items):
        return Or(items[0], items[1])

    def enter(self, items):
        return Enter(items[0])

    def exit(self, items):
        return Exit(items[0])

    def before(self, items):
        return Before(items[0])

    def after(self, items):
        return After(items[0])

    def between(self, items):
        return Between(items[0], items[1])
