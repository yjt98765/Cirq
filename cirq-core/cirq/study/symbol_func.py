from typing import AbstractSet

import sympy

from cirq import protocols


class SymbolFunc:
    """A "lambdified" symbolic expression that is faster for parameter resolution."""

    def __init__(self, expr: sympy.Basic) -> None:
        self.expr = expr
        self.param_set = protocols.parameter_names(expr)
        self.params = sorted(self.param_set)
        self.func = sympy.lambdify(self.params, expr)

    def _is_parameterized_(self) -> bool:
        return True

    def _parameter_names_(self) -> AbstractSet[str]:
        return self.param_set

    def _resolve_parameters_(self, resolver: cirq.ParamResolver, recursive: bool) -> float:
        args = [resolver.value_of(param, recursive=recursive) for param in self.params]
        return self.func(*args)

    def __repr__(self) -> str:
        return f'SymbolFunc({self.expr!r})'
