from sympy import pprint
from sympy.core.parameters import global_parameters

from matchpy import to_expression
from rubi_rules.base_objects import rubi_integrate, _CACHED_REPLACER, _preprocess_integrate, reset_cache, Int
from sympy.abc import x, y, z, a, b, c

from sympy_objects.conversion import matchpy_to_sympy

global_parameters.exp_is_pow = True

if __name__ == "__main__":
    res = rubi_integrate(x/(x**2 + 1), x, "**/r_1_1_**")

    from rubi_rules.base_objects import rubi_integrate, _CACHED_REPLACER, _preprocess_integrate, reset_cache, Int
    res = rubi_integrate(x/(x**2 + 1), x, "**/r_1_1_2**")

    matches = list(_CACHED_REPLACER.matcher.match(to_expression(Int(x/(x**2 + 1), x))))
    print(res)

    for f, subst in matches:
        try:
            pprint(matchpy_to_sympy(f(**subst)))
        except Exception:
            print("=== EXCEPTION ===")
            print(f(**subst))
