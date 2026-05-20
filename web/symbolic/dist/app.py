from sympy.parsing.sympy_parser import (
    parse_expr,
    standard_transformations,
    implicit_multiplication_application,
    function_exponentiation,
    split_symbols,
)
from sympy import Expr, solve
import keyword
import re
from flask import Flask, request, render_template

TRANSFORMATIONS = standard_transformations + (
    split_symbols,
    implicit_multiplication_application,
    function_exponentiation,
)

app = Flask(__name__)


class ExprError(Exception, object): ...


def solve_expression(expression: str) -> dict[str, list[str]]:
    try:
        expr: Expr | None = parse_expr(expression, transformations=TRANSFORMATIONS)
    except (SyntaxError, TypeError) as e:
        raise ExprError(f"Failed to parse expression {expression}")

    if expr is None:
        raise ExprError(f"Failed to parse expression {expression}")

    if len(expr.free_symbols) > 3:
        raise ExprError(
            f"Too many free variables: {expr.free_symbols}. Maximum 3 free variables"
        )

    results: dict[str, list[str]] = {}
    for free_symbol in expr.free_symbols:
        try:
            _, solutions_set = solve(expr, free_symbol, set=True)
            if not solutions_set:
                results[str(free_symbol)] = []
                continue
            solution_strs = [str(sol[0]) for sol in solutions_set]
            results[str(free_symbol)] = solution_strs
        except NotImplementedError as e:
            raise ExprError(f"Operation is not implemented {e}")

    return results


def is_safe_expression(expression: str) -> bool:
    for kw in keyword.kwlist:
        if re.search(rf"\b{re.escape(kw)}\b", expression):
            return False

    for kw in keyword.softkwlist:
        if re.search(rf"\b{re.escape(kw)}\b", expression):
            return False

    return True


@app.route("/solve", methods=["POST"])
def POST_solve():
    data = request.json
    if "expression" not in data:
        return {"error": "missing expression key in JSON body"}, 400

    expression = data["expression"]
    if not is_safe_expression(expression):
        return {"error": "expression cannot be parsed safely"}, 400

    try:
        solved_expression = solve_expression(expression)
    except ExprError as e:
        return {"error": str(e)}, 400

    return {"result": solved_expression}, 200


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
