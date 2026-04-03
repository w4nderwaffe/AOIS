from implicants import (
    build_coverage_table,
    build_initial_implicants_from_sdnf,
    find_essential_implicants,
    find_prime_implicants,
    find_redundant_implicants,
    pattern_to_expression,
)
from models import Implicant, MinimizationResult, TruthTable
from normal_forms import build_sdnf


def _minterm_indices(table: TruthTable) -> list[int]:
    return [row.index for row in table.rows if row.result == 1]


def _covers_all(selected: list[Implicant], minterm_indices: list[int]) -> bool:
    covered: set[int] = set()
    for item in selected:
        covered.update(item.covered_indices)
    return set(minterm_indices).issubset(covered)


def select_implicants_greedy(prime_implicants: list[Implicant], minterm_indices: list[int]) -> list[Implicant]:
    remaining = set(minterm_indices)
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


def implicants_to_expression(items: list[Implicant], variables: list[str]) -> str:
    if len(items) == 0:
        return "0"

    parts = [pattern_to_expression(item.pattern, variables) for item in items]
    return "|".join(parts)


def minimize_by_calculation(table: TruthTable) -> MinimizationResult:
    original_expression = build_sdnf(table)
    minterm_indices = _minterm_indices(table)

    if len(minterm_indices) == 0:
        return MinimizationResult(
            original_expression=original_expression,
            gluing_steps=[],
            prime_implicants=[],
            essential_implicants=[],
            redundant_implicants=[],
            minimized_expression="0",
            coverage_table=[],
        )

    if len(minterm_indices) == len(table.rows):
        all_pattern = "X" * len(table.variables)
        universal = Implicant(pattern=all_pattern, covered_indices=minterm_indices[:])
        return MinimizationResult(
            original_expression=original_expression,
            gluing_steps=[],
            prime_implicants=[universal],
            essential_implicants=[universal],
            redundant_implicants=[],
            minimized_expression="1",
            coverage_table=[[1 for _ in minterm_indices]],
        )

    initial = build_initial_implicants_from_sdnf(table)
    gluing_steps, prime_implicants = find_prime_implicants(initial)
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

    selected_keys = set()
    unique_selected: list[Implicant] = []
    for item in selected:
        key = (item.pattern, tuple(item.covered_indices))
        if key not in selected_keys:
            selected_keys.add(key)
            unique_selected.append(item)

    redundant_implicants = find_redundant_implicants(prime_implicants, unique_selected, minterm_indices)

    return MinimizationResult(
        original_expression=original_expression,
        gluing_steps=gluing_steps,
        prime_implicants=prime_implicants,
        essential_implicants=unique_selected,
        redundant_implicants=redundant_implicants,
        minimized_expression=implicants_to_expression(unique_selected, table.variables),
        coverage_table=[],
    )


def minimize_by_calculation_table(table: TruthTable) -> MinimizationResult:
    original_expression = build_sdnf(table)
    minterm_indices = _minterm_indices(table)

    if len(minterm_indices) == 0:
        return MinimizationResult(
            original_expression=original_expression,
            gluing_steps=[],
            prime_implicants=[],
            essential_implicants=[],
            redundant_implicants=[],
            minimized_expression="0",
            coverage_table=[],
        )

    if len(minterm_indices) == len(table.rows):
        all_pattern = "X" * len(table.variables)
        universal = Implicant(pattern=all_pattern, covered_indices=minterm_indices[:])
        table_data = [[1 for _ in minterm_indices]]
        return MinimizationResult(
            original_expression=original_expression,
            gluing_steps=[],
            prime_implicants=[universal],
            essential_implicants=[universal],
            redundant_implicants=[],
            minimized_expression="1",
            coverage_table=table_data,
        )

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

    selected_keys = set()
    unique_selected: list[Implicant] = []
    for item in selected:
        key = (item.pattern, tuple(item.covered_indices))
        if key not in selected_keys:
            selected_keys.add(key)
            unique_selected.append(item)

    redundant_implicants = find_redundant_implicants(prime_implicants, unique_selected, minterm_indices)

    return MinimizationResult(
        original_expression=original_expression,
        gluing_steps=gluing_steps,
        prime_implicants=prime_implicants,
        essential_implicants=unique_selected,
        redundant_implicants=redundant_implicants,
        minimized_expression=implicants_to_expression(unique_selected, table.variables),
        coverage_table=coverage_table,
    )