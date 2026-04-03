from ast_nodes import AstNode
from errors import TruthTableError
from models import TruthTable, TruthTableRow


def extract_variables(root: AstNode) -> list[str]:
    variables = sorted(root.collect_variables())
    if len(variables) == 0:
        raise TruthTableError("В выражении нет переменных")
    if len(variables) > 5:
        raise TruthTableError("Допускается не более 5 переменных")
    return variables


def generate_assignments(variables: list[str]) -> list[dict[str, int]]:
    if len(variables) == 0:
        raise TruthTableError("Список переменных пуст")
    if len(variables) > 5:
        raise TruthTableError("Допускается не более 5 переменных")

    assignments: list[dict[str, int]] = []
    total = 1 << len(variables)

    for mask in range(total):
        values: dict[str, int] = {}
        for index, variable in enumerate(variables):
            shift = len(variables) - 1 - index
            values[variable] = (mask >> shift) & 1
        assignments.append(values)

    return assignments


def build_truth_table(root: AstNode) -> TruthTable:
    variables = extract_variables(root)
    expressions = root.collect_subexpressions()
    assignments = generate_assignments(variables)
    rows: list[TruthTableRow] = []

    for index, values in enumerate(assignments):
        expression_values: dict[str, int] = {}
        result = root.fill_expression_values(values, expression_values)

        if result not in (0, 1):
            raise TruthTableError("Значение функции должно быть 0 или 1")

        if len(expressions) > 0:
            for expression in expressions:
                if expression not in expression_values:
                    raise TruthTableError(
                        f"Не вычислено значение подвыражения '{expression}'"
                    )

        rows.append(
            TruthTableRow(
                index=index,
                values=dict(values),
                expression_values=dict(expression_values),
                result=result,
            )
        )

    return TruthTable(variables=variables, expressions=expressions, rows=rows)