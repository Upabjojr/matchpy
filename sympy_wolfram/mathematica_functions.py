import sympy

from sympy_wolfram import MathematicaExpr


class Gamma(MathematicaExpr):
    def _evaluate(self, **kwargs):
        if len(self.args) == 1:
            return sympy.gamma(self.args[0])
        elif len(self.args) == 2:
            return sympy.uppergamma(self.args[0], self.args[1])
        else:
            raise NotImplementedError
