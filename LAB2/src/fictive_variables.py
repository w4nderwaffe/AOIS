from models import TruthTable


def is_variable_fictive(table: TruthTable, variable: str) -> bool:
    if variable not in table.variables:
        raise ValueError(f"Переменная '{variable}' отсутствует в таблице истинности")

    rows_by_values: dict[tuple[int, ...], int] = {}

    for row in table.rows:
        key_parts: list[int] = []
        for current_variable in table.variables:
            if current_variable != variable:
                key_parts.append(row.values[current_variable])
        key = tuple(key_parts)

        if key not in rows_by_values:
            rows_by_values[key] = row.result
        elif rows_by_values[key] != row.result:
            return False

    return True


def find_fictive_variables(table: TruthTable) -> list[str]:
    result: list[str] = []

    for variable in table.variables:
        if is_variable_fictive(table, variable):
            result.append(variable)

    return result