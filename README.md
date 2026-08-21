# Event QL

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![Parser](https://img.shields.io/badge/parser-Lark-green.svg)
![Status](https://img.shields.io/badge/status-experimental-yellow.svg)

A lightweight **domain-specific language (DSL)** for defining and evaluating signal transformations over structured numeric data.

It provides a declarative syntax for expressing:
- statistical filters
- conditional aggregations
- composable signal functions

All compiled through a **grammar → AST → evaluation pipeline**.

---

## Install

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e .
```

## Example

```python
import torch

from eventql import ASTBuilder, compiler, parser

tree = parser.parse("C(x) > 2")
node = ASTBuilder().transform(tree)
expression = compiler(node)
result = expression.evaluate({"x": torch.tensor([1.0, 2.0, 3.0])})
```

The current grammar supports signal names, numeric constants, differences,
cumulative sums, comparisons, and Boolean `&`/`|` composition.

---

## Project structure

```
src/eventql/
├── ast/                    # AST nodes
├── compiler/               # Typed expression wrapper
├── parser/                 # Lark grammar and transformer
├── runtime/                # PyTorch evaluator
└── semantics/              # Type inference
```

---

## DSL syntax

Examples: `D(x)`, `C(x) > 2`, and `(x > 0) & (y < 5)`.

---

## AST Design

Core node types:

| Node Type        | Purpose                          |
|------------------|----------------------------------|
| Signal           | Named signal reference           |
| Constant         | Numeric literal                  |
| BinaryOp         | Arithmetic / comparisons         |
| Diff / Cumsum    | Temporal transforms               |
| Eq / Lt / Gt     | Comparisons                       |
| And / Or         | Boolean composition               |

---

## Execution model

```
text → parse tree → AST → type inference → PyTorch evaluation
```

## Design Philosophy

- Compiler architecture for data transforms
- Signal-first composability
- Vectorized execution model

---

## Dependencies

- Python ≥ 3.10
- Lark parser
- PyTorch

```bash
python -m pip install -e .
```

---

## License

MIT
