# compiler.py

from eventql.compiler.expression import Expression
from eventql.runtime.interpreter import expand_events, eval_value
from eventql.semantics.infer_type import infer_type

def compiler(node, events):

    t = infer_type(node)

    return Expression(
        node=node,
        type=t,
        events=events,
        event_resolver=expand_events,
        evaluator=eval_value
    )