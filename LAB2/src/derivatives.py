from itertools import combinations, product

from ast_nodes import AstNode
from models import DerivativeResult, TruthTable, TruthTableRow
from normal_forms import build_sdnf


def flip_variables(values: dict[str, int], variables: list[str]) -> dict[str, int]:
    result = dict(values)

    for variable in variables:
        if variable not in result:
            raise ValueError(f"Переменная '{variable}' отсутствует в наборе значений")
        result[variable] = 1 - result[variable]

    return result


def _derivative_value(root: AstNode, values: dict[str, int], diff_variables: list[str]) -> int:
    total = 0

    for mask in product((0, 1), repeat=len(diff_variables)):
        current = dict(values)
        for bit, variable in zip(mask, diff_variables):
            if bit == 1:
                current[variable] = 1 - current[variable]
        total ^= root.evaluate(current)

    return total


def build_derivative_truth_table(
    root: AstNode,
    base_variables: list[str],
    diff_variables: list[str],
) -> TruthTable:
    total = 1 << len(base_variables)
    rows: list[TruthTableRow] = []

    if len(diff_variables) == 1:
        derivative_expression = f"D[{diff_variables[0]}]"
    else:
        derivative_expression = "D[" + ",".join(diff_variables) + "]"

    expressions = [derivative_expression]

    for index in range(total):
        values: dict[str, int] = {}
        for position, variable in enumerate(base_variables):
            shift = len(base_variables) - 1 - position
            values[variable] = (index >> shift) & 1

        result = _derivative_value(root, values, diff_variables)
        expression_values = {derivative_expression: result}

        rows.append(
            TruthTableRow(
                index=index,
                values=values,
                expression_values=expression_values,
                result=result,
            )
        )

    return TruthTable(variables=base_variables[:], expressions=expressions, rows=rows)


def build_derivative_expression(table: TruthTable) -> str:
    return build_sdnf(table)


def build_partial_derivative(root: AstNode, variables: list[str], by_variable: str) -> DerivativeResult:
    if by_variable not in variables:
        raise ValueError(f"Переменная '{by_variable}' отсутствует в списке переменных")

    table = build_derivative_truth_table(root, variables, [by_variable])
    expression = build_derivative_expression(table)

    return DerivativeResult(
        by_variables=[by_variable],
        truth_table=table,
        expression=expression,
    )


def build_mixed_derivative(root: AstNode, variables: list[str], by_variables: list[str]) -> DerivativeResult:
    for variable in by_variables:
        if variable not in variables:
            raise ValueError(f"Переменная '{variable}' отсутствует в списке переменных")

    unique_variables = list(dict.fromkeys(by_variables))
    table = build_derivative_truth_table(root, variables, unique_variables)
    expression = build_derivative_expression(table)

    return DerivativeResult(
        by_variables=unique_variables,
        truth_table=table,
        expression=expression,
    )


def build_all_required_derivatives(root: AstNode, variables: list[str]) -> list[DerivativeResult]:
    results: list[DerivativeResult] = []

    for variable in variables:
        results.append(build_partial_derivative(root, variables, variable))

    max_order = min(4, len(variables))
    for size in range(2, max_order + 1):
        for combo in combinations(variables, size):
            results.append(build_mixed_derivative(root, variables, list(combo)))

    return results