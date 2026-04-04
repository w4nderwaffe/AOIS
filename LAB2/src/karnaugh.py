from implicants import pattern_to_expression
from minimization import (
    implicants_to_expression_cnf,
    implicants_to_expression_dnf,
    select_implicants_greedy,
)
from models import Implicant, KarnaughGroup, KarnaughResult, TruthTable


def gray_code(bits: int) -> list[str]:
    if bits <= 0:
        return [""]

    result = ["0", "1"]
    for _ in range(2, bits + 1):
        left = ["0" + item for item in result]
        right = ["1" + item for item in reversed(result)]
        result = left + right
    return result


def _split_variable_counts(count: int) -> tuple[int, int]:
    if count <= 1:
        return 1, 0
    row_bits = count // 2
    col_bits = count - row_bits
    return row_bits, col_bits


def _index_from_bits(bits: str) -> int:
    if bits == "":
        return 0
    return int(bits, 2)


def karnaugh_cell_indices(table: TruthTable) -> list[list[int]]:
    variable_count = len(table.variables)

    if variable_count == 1:
        return [[0, 1]]

    row_bits, col_bits = _split_variable_counts(variable_count)
    row_codes = gray_code(row_bits)
    col_codes = gray_code(col_bits)
    indices: list[list[int]] = []

    for row_code in row_codes:
        row: list[int] = []
        for col_code in col_codes:
            bits = row_code + col_code
            row.append(_index_from_bits(bits))
        indices.append(row)

    return indices


def build_karnaugh_map(table: TruthTable) -> list[list[int]]:
    index_map = {row.index: row.result for row in table.rows}
    cell_indices = karnaugh_cell_indices(table)

    result: list[list[int]] = []
    for row in cell_indices:
        result.append([index_map[index] for index in row])

    return result


def _combine_patterns_if_adjacent(left: str, right: str) -> str | None:
    if len(left) != len(right):
        return None

    diff_positions: list[int] = []
    for index, (left_char, right_char) in enumerate(zip(left, right)):
        if left_char != right_char:
            if left_char == "X" or right_char == "X":
                return None
            diff_positions.append(index)

    if len(diff_positions) != 1:
        return None

    position = diff_positions[0]
    result = list(left)
    result[position] = "X"
    return "".join(result)


def _build_candidate_groups(indices: list[int], variable_count: int) -> list[Implicant]:
    if len(indices) == 0:
        return []

    current = [
        Implicant(pattern=format(index, f"0{variable_count}b"), covered_indices=[index])
        for index in indices
    ]
    all_items: dict[tuple[str, tuple[int, ...]], Implicant] = {
        (item.pattern, tuple(item.covered_indices)): item for item in current
    }

    while True:
        next_items: list[Implicant] = []

        for left_index in range(len(current)):
            for right_index in range(left_index + 1, len(current)):
                left = current[left_index]
                right = current[right_index]
                glued = _combine_patterns_if_adjacent(left.pattern, right.pattern)
                if glued is None:
                    continue

                covered = sorted(set(left.covered_indices) | set(right.covered_indices))
                if len(covered) & (len(covered) - 1) != 0:
                    continue

                item = Implicant(pattern=glued, covered_indices=covered)
                key = (item.pattern, tuple(item.covered_indices))
                if key not in all_items:
                    all_items[key] = item
                    next_items.append(item)

        if len(next_items) == 0:
            break

        current = next_items

    indices_set = set(indices)
    filtered: list[Implicant] = []

    for item in all_items.values():
        if set(item.covered_indices).issubset(indices_set):
            filtered.append(item)

    return sorted(
        filtered,
        key=lambda item: (-len(item.covered_indices), item.pattern, item.covered_indices),
    )


def _pattern_to_cnf_expression(pattern: str, variables: list[str]) -> str:
    parts: list[str] = []

    for char, variable in zip(pattern, variables):
        if char == "0":
            parts.append(variable)
        elif char == "1":
            parts.append(f"!{variable}")

    if len(parts) == 0:
        return "0"
    if len(parts) == 1:
        return parts[0]
    return "(" + "|".join(parts) + ")"


def _find_groups_for_ones(table: TruthTable) -> list[KarnaughGroup]:
    minterms = [row.index for row in table.rows if row.result == 1]
    variable_count = len(table.variables)

    if len(minterms) == 0:
        return []

    if len(minterms) == len(table.rows):
        return [
            KarnaughGroup(
                cells=minterms[:],
                pattern="X" * variable_count,
                expression="1",
            )
        ]

    candidates = _build_candidate_groups(minterms, variable_count)
    selected = select_implicants_greedy(candidates, minterms)

    groups: list[KarnaughGroup] = []
    for item in selected:
        groups.append(
            KarnaughGroup(
                cells=item.covered_indices[:],
                pattern=item.pattern,
                expression=pattern_to_expression(item.pattern, table.variables),
            )
        )

    return groups


def _find_groups_for_zeros(table: TruthTable) -> list[KarnaughGroup]:
    maxterms = [row.index for row in table.rows if row.result == 0]
    variable_count = len(table.variables)

    if len(maxterms) == 0:
        return []

    if len(maxterms) == len(table.rows):
        return [
            KarnaughGroup(
                cells=maxterms[:],
                pattern="X" * variable_count,
                expression="0",
            )
        ]

    candidates = _build_candidate_groups(maxterms, variable_count)
    selected = select_implicants_greedy(candidates, maxterms)

    groups: list[KarnaughGroup] = []
    for item in selected:
        groups.append(
            KarnaughGroup(
                cells=item.covered_indices[:],
                pattern=item.pattern,
                expression=_pattern_to_cnf_expression(item.pattern, table.variables),
            )
        )

    return groups


def find_karnaugh_groups(table: TruthTable) -> tuple[list[KarnaughGroup], list[KarnaughGroup]]:
    return _find_groups_for_ones(table), _find_groups_for_zeros(table)


def minimize_by_karnaugh(table: TruthTable) -> KarnaughResult:
    minterms = [row.index for row in table.rows if row.result == 1]
    maxterms = [row.index for row in table.rows if row.result == 0]

    if len(minterms) == 0:
        return KarnaughResult(
            map_rows=build_karnaugh_map(table),
            groups_for_ones=[],
            groups_for_zeros=[
                KarnaughGroup(
                    cells=maxterms[:],
                    pattern="X" * len(table.variables),
                    expression="0",
                )
            ],
            minimized_dnf="0",
            minimized_cnf="0",
        )

    if len(maxterms) == 0:
        return KarnaughResult(
            map_rows=build_karnaugh_map(table),
            groups_for_ones=[
                KarnaughGroup(
                    cells=minterms[:],
                    pattern="X" * len(table.variables),
                    expression="1",
                )
            ],
            groups_for_zeros=[],
            minimized_dnf="1",
            minimized_cnf="1",
        )

    groups_for_ones, groups_for_zeros = find_karnaugh_groups(table)

    dnf_implicants = [
        Implicant(pattern=group.pattern, covered_indices=group.cells[:])
        for group in groups_for_ones
    ]
    cnf_implicants = [
        Implicant(pattern=group.pattern, covered_indices=group.cells[:])
        for group in groups_for_zeros
    ]

    return KarnaughResult(
        map_rows=build_karnaugh_map(table),
        groups_for_ones=groups_for_ones,
        groups_for_zeros=groups_for_zeros,
        minimized_dnf=implicants_to_expression_dnf(dnf_implicants, table.variables),
        minimized_cnf=implicants_to_expression_cnf(cnf_implicants, table.variables),
    )