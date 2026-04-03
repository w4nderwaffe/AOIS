from models import TruthTable, ZhegalkinTerm


def build_difference_triangle(values: list[int]) -> list[list[int]]:
    if len(values) == 0:
        return []

    triangle: list[list[int]] = [values[:]]
    current = values[:]

    while len(current) > 1:
        next_row: list[int] = []
        for index in range(len(current) - 1):
            next_row.append(current[index] ^ current[index + 1])
        triangle.append(next_row)
        current = next_row

    return triangle


def extract_zhegalkin_coefficients(values: list[int]) -> list[int]:
    triangle = build_difference_triangle(values)
    coefficients: list[int] = []

    for row in triangle:
        coefficients.append(row[0])

    return coefficients


def coefficient_index_to_variables(index: int, variables: list[str]) -> list[str]:
    result: list[str] = []
    count = len(variables)

    for position, variable in enumerate(variables):
        shift = count - 1 - position
        if ((index >> shift) & 1) == 1:
            result.append(variable)

    return result


def build_zhegalkin_terms(table: TruthTable) -> list[ZhegalkinTerm]:
    coefficients = extract_zhegalkin_coefficients(table.results_vector())
    terms: list[ZhegalkinTerm] = []

    for index, coefficient in enumerate(coefficients):
        if coefficient == 1:
            variables = coefficient_index_to_variables(index, table.variables)
            terms.append(ZhegalkinTerm(variables=variables))

    return terms


def format_zhegalkin_polynomial(terms: list[ZhegalkinTerm]) -> str:
    if len(terms) == 0:
        return "0"

    parts: list[str] = []
    for term in terms:
        if term.is_constant_one():
            parts.append("1")
        else:
            parts.append("*".join(term.variables))

    return " ⊕ ".join(parts)


def build_zhegalkin_polynomial(table: TruthTable) -> str:
    terms = build_zhegalkin_terms(table)
    return format_zhegalkin_polynomial(terms)