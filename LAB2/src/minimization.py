from implicants import (
    build_coverage_table,
    build_initial_implicants_from_sdnf,
    find_essential_implicants,
    find_prime_implicants,
    find_redundant_implicants,
    pattern_to_expression,
)
from models import Implicant, MinimizationResult, TruthTable
from normal_forms import build_sdnf, build_sknf


def _minterm_indices(table: TruthTable) -> list[int]:
    return [row.index for row in table.rows if row.result == 1]


def _maxterm_indices(table: TruthTable) -> list[int]:
    return [row.index for row in table.rows if row.result == 0]


def _covers_all(selected: list[Implicant], indices: list[int]) -> bool:
    covered: set[int] = set()
    for item in selected:
        covered.update(item.covered_indices)
    return set(indices).issubset(covered)


def select_implicants_greedy(prime_implicants: list[Implicant], indices: list[int]) -> list[Implicant]:
    remaining = set(indices)
    selected: list[Implicant] = []

    while len(remaining) > 0:
        best_item = None
        best_cover: set[int] = set()

        for item in prime_implicants:
            current_cover = set(item.covered_indices) & remaining
            if len(current_cover) > len(best_cover):
                best_item = item
                best_cover = current_cover
            elif len(current_cover) == len(best_cover) and len(current_cover) > 0 and best_item is not None:
                if item.rank() < best_item.rank():
                    best_item = item
                    best_cover = current_cover

        if best_item is None or len(best_cover) == 0:
            break

        key = (best_item.pattern, tuple(best_item.covered_indices))
        if key not in {(item.pattern, tuple(item.covered_indices)) for item in selected}:
            selected.append(best_item)

        remaining -= best_cover

    return selected


def implicants_to_expression_dnf(items: list[Implicant], variables: list[str]) -> str:
    if len(items) == 0:
        return "0"

    parts = [pattern_to_expression(item.pattern, variables) for item in items]
    return "|".join(parts)


def _pattern_to_cnf_expression(pattern: str, variables: list[str]) -> str:
    if len(pattern) != len(variables):
        raise ValueError("Длина шаблона должна совпадать с количеством переменных")

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


def implicants_to_expression_cnf(items: list[Implicant], variables: list[str]) -> str:
    if len(items) == 0:
        return "1"

    parts = [_pattern_to_cnf_expression(item.pattern, variables) for item in items]
    return "&".join(parts)


def _build_initial_implicants_from_sknf(table: TruthTable) -> list[Implicant]:
    implicants: list[Implicant] = []

    for row in table.rows:
        if row.result == 0:
            pattern = format(row.index, f"0{len(table.variables)}b")
            implicants.append(Implicant(pattern=pattern, covered_indices=[row.index]))

    return implicants


def _deduplicate_selected(items: list[Implicant]) -> list[Implicant]:
    selected_keys = set()
    result: list[Implicant] = []

    for item in items:
        key = (item.pattern, tuple(item.covered_indices))
        if key not in selected_keys:
            selected_keys.add(key)
            result.append(item)

    return result


def _solve_dnf_side(table: TruthTable) -> tuple[list, list, list, list, list, str]:
    minterm_indices = _minterm_indices(table)

    if len(minterm_indices) == 0:
        return [], [], [], [], [], "0"

    if len(minterm_indices) == len(table.rows):
        all_pattern = "X" * len(table.variables)
        universal = Implicant(pattern=all_pattern, covered_indices=minterm_indices[:])
        return [], [universal], [universal], [], [[1 for _ in minterm_indices]], "1"

    initial = build_initial_implicants_from_sdnf(table)
    gluing_steps, prime_implicants = find_prime_implicants(initial)
    coverage_table = build_coverage_table(prime_implicants, minterm_indices)
    essential_implicants = find_essential_implicants(prime_implicants, minterm_indices)

    selected = essential_implicants[:]
    if not _covers_all(selected, minterm_indices):
        not_selected = [
            item
            for item in prime_implicants
            if (item.pattern, tuple(item.covered_indices))
            not in {(current.pattern, tuple(current.covered_indices)) for current in selected}
        ]
        selected.extend(select_implicants_greedy(not_selected, minterm_indices))

    selected = _deduplicate_selected(selected)
    redundant_implicants = find_redundant_implicants(prime_implicants, selected, minterm_indices)
    minimized_dnf = implicants_to_expression_dnf(selected, table.variables)

    return gluing_steps, prime_implicants, selected, redundant_implicants, coverage_table, minimized_dnf


def _solve_cnf_side(table: TruthTable) -> tuple[list, list, list, list, list, str]:
    maxterm_indices = _maxterm_indices(table)

    if len(maxterm_indices) == 0:
        return [], [], [], [], [], "1"

    if len(maxterm_indices) == len(table.rows):
        all_pattern = "X" * len(table.variables)
        universal = Implicant(pattern=all_pattern, covered_indices=maxterm_indices[:])
        return [], [universal], [universal], [], [[1 for _ in maxterm_indices]], "0"

    initial = _build_initial_implicants_from_sknf(table)
    gluing_steps, prime_implicants = find_prime_implicants(initial)
    coverage_table = build_coverage_table(prime_implicants, maxterm_indices)
    essential_implicants = find_essential_implicants(prime_implicants, maxterm_indices)

    selected = essential_implicants[:]
    if not _covers_all(selected, maxterm_indices):
        not_selected = [
            item
            for item in prime_implicants
            if (item.pattern, tuple(item.covered_indices))
            not in {(current.pattern, tuple(current.covered_indices)) for current in selected}
        ]
        selected.extend(select_implicants_greedy(not_selected, maxterm_indices))

    selected = _deduplicate_selected(selected)
    redundant_implicants = find_redundant_implicants(prime_implicants, selected, maxterm_indices)
    minimized_cnf = implicants_to_expression_cnf(selected, table.variables)

    return gluing_steps, prime_implicants, selected, redundant_implicants, coverage_table, minimized_cnf


def minimize_by_calculation(table: TruthTable) -> MinimizationResult:
    dnf_gluing_steps, prime_implicants_dnf, selected_dnf, redundant_dnf, _, minimized_dnf = _solve_dnf_side(table)
    cnf_gluing_steps, prime_implicants_cnf, selected_cnf, redundant_cnf, _, minimized_cnf = _solve_cnf_side(table)

    return MinimizationResult(
        original_sdnf=build_sdnf(table),
        original_sknf=build_sknf(table),
        dnf_gluing_steps=dnf_gluing_steps,
        cnf_gluing_steps=cnf_gluing_steps,
        prime_implicants_dnf=prime_implicants_dnf,
        prime_implicants_cnf=prime_implicants_cnf,
        selected_implicants_dnf=selected_dnf,
        selected_implicants_cnf=selected_cnf,
        redundant_implicants_dnf=redundant_dnf,
        redundant_implicants_cnf=redundant_cnf,
        coverage_table_dnf=[],
        coverage_table_cnf=[],
        minimized_dnf=minimized_dnf,
        minimized_cnf=minimized_cnf,
    )


def minimize_by_calculation_table(table: TruthTable) -> MinimizationResult:
    dnf_gluing_steps, prime_implicants_dnf, selected_dnf, redundant_dnf, coverage_dnf, minimized_dnf = _solve_dnf_side(table)
    cnf_gluing_steps, prime_implicants_cnf, selected_cnf, redundant_cnf, coverage_cnf, minimized_cnf = _solve_cnf_side(table)

    return MinimizationResult(
        original_sdnf=build_sdnf(table),
        original_sknf=build_sknf(table),
        dnf_gluing_steps=dnf_gluing_steps,
        cnf_gluing_steps=cnf_gluing_steps,
        prime_implicants_dnf=prime_implicants_dnf,
        prime_implicants_cnf=prime_implicants_cnf,
        selected_implicants_dnf=selected_dnf,
        selected_implicants_cnf=selected_cnf,
        redundant_implicants_dnf=redundant_dnf,
        redundant_implicants_cnf=redundant_cnf,
        coverage_table_dnf=coverage_dnf,
        coverage_table_cnf=coverage_cnf,
        minimized_dnf=minimized_dnf,
        minimized_cnf=minimized_cnf,
    )