# expression.py

from dataclasses import dataclass

@dataclass
class Expression:
    node: object
    type: object
    events: dict
    event_resolver: callable
    evaluator: callable


    def evaluate(self, ctx):
        resolved = self.event_resolver(self.node, self.events)
        return self.evaluator(resolved, ctx)

