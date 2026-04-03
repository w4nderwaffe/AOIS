from models import GluingStep, Implicant, TruthTable


def minterm_index_to_pattern(index: int, var_count: int) -> str:
    if var_count <= 0:
        raise ValueError("Количество переменных должно быть положительным")
    if index < 0 or index >= (1 << var_count):
        raise ValueError("Индекс минтерма вне допустимого диапазона")
    return format(index, f"0{var_count}b")


def patterns_differ_by_one_bit(left: str, right: str) -> bool:
    if len(left) != len(right):
        raise ValueError("Шаблоны должны иметь одинаковую длину")

    diff_count = 0
    for left_char, right_char in zip(left, right):
        if left_char != right_char:
            if left_char == "X" or right_char == "X":
                return False
            diff_count += 1
            if diff_count > 1:
                return False

    return diff_count == 1


def glue_patterns(left: str, right: str) -> str:
    if len(left) != len(right):
        raise ValueError("Шаблоны должны иметь одинаковую длину")
    if not patterns_differ_by_one_bit(left, right):
        raise ValueError("Шаблоны нельзя склеить")

    result: list[str] = []
    for left_char, right_char in zip(left, right):
        result.append(left_char if left_char == right_char else "X")
    return "".join(result)


def pattern_covers_index(pattern: str, index: int, var_count: int) -> bool:
    bits = minterm_index_to_pattern(index, var_count)
    for pattern_char, bit_char in zip(pattern, bits):
        if pattern_char != "X" and pattern_char != bit_char:
            return False
    return True


def pattern_to_expression(pattern: str, variables: list[str]) -> str:
    if len(pattern) != len(variables):
        raise ValueError("Длина шаблона должна совпадать с количеством переменных")

    parts: list[str] = []
    for char, variable in zip(pattern, variables):
        if char == "1":
            parts.append(variable)
        elif char == "0":
            parts.append(f"!{variable}")

    if len(parts) == 0:
        return "1"
    if len(parts) == 1:
        return parts[0]
    return "(" + "&".join(parts) + ")"


def build_initial_implicants_from_sdnf(table: TruthTable) -> list[Implicant]:
    implicants: list[Implicant] = []

    for row in table.rows:
        if row.result == 1:
            pattern = minterm_index_to_pattern(row.index, len(table.variables))
            implicants.append(Implicant(pattern=pattern, covered_indices=[row.index]))

    return implicants


def remove_duplicate_implicants(items: list[Implicant]) -> list[Implicant]:
    unique: dict[tuple[str, tuple[int, ...]], Implicant] = {}

    for item in items:
        key = (item.pattern, tuple(sorted(item.covered_indices)))
        if key not in unique:
            unique[key] = Implicant(
                pattern=item.pattern,
                covered_indices=sorted(item.covered_indices),
            )

    return sorted(unique.values(), key=lambda item: (item.pattern, item.covered_indices))


def _merge_covered_indices(left: list[int], right: list[int]) -> list[int]:
    return sorted(set(left) | set(right))


def find_prime_implicants(initial: list[Implicant]) -> tuple[list[GluingStep], list[Implicant]]:
    if len(initial) == 0:
        return [], []

    current = remove_duplicate_implicants(initial)
    steps: list[GluingStep] = []
    prime_implicants: list[Implicant] = []

    while True:
        used_indices: set[int] = set()
        next_items: list[Implicant] = []
        source_patterns: list[str] = []
        result_patterns: list[str] = []

        for left_index in range(len(current)):
            for right_index in range(left_index + 1, len(current)):
                left_item = current[left_index]
                right_item = current[right_index]

                if patterns_differ_by_one_bit(left_item.pattern, right_item.pattern):
                    glued_pattern = glue_patterns(left_item.pattern, right_item.pattern)
                    covered = _merge_covered_indices(
                        left_item.covered_indices,
                        right_item.covered_indices,
                    )
                    next_items.append(Implicant(pattern=glued_pattern, covered_indices=covered))
                    used_indices.add(left_index)
                    used_indices.add(right_index)
                    source_patterns.append(f"{left_item.pattern}+{right_item.pattern}")
                    result_patterns.append(glued_pattern)

        for index, item in enumerate(current):
            if index not in used_indices:
                prime_implicants.append(item)

        next_items = remove_duplicate_implicants(next_items)

        if len(source_patterns) > 0:
            steps.append(
                GluingStep(
                    source_patterns=sorted(set(source_patterns)),
                    result_patterns=sorted(set(result_patterns)),
                )
            )

        if len(next_items) == 0:
            break

        current = next_items

    prime_implicants = remove_duplicate_implicants(prime_implicants)
    return steps, prime_implicants


def build_coverage_table(prime_implicants: list[Implicant], minterm_indices: list[int]) -> list[list[int]]:
    if len(prime_implicants) == 0 or len(minterm_indices) == 0:
        return []

    table: list[list[int]] = []
    for implicant in prime_implicants:
        row: list[int] = []
        covered_set = set(implicant.covered_indices)
        for index in minterm_indices:
            row.append(1 if index in covered_set else 0)
        table.append(row)

    return table


def find_essential_implicants(prime_implicants: list[Implicant], minterm_indices: list[int]) -> list[Implicant]:
    if len(prime_implicants) == 0 or len(minterm_indices) == 0:
        return []

    essential_indices: set[int] = set()

    for minterm in minterm_indices:
        covering_rows: list[int] = []
        for row_index, implicant in enumerate(prime_implicants):
            if minterm in implicant.covered_indices:
                covering_rows.append(row_index)

        if len(covering_rows) == 1:
            essential_indices.add(covering_rows[0])

    return [prime_implicants[index] for index in sorted(essential_indices)]


def find_redundant_implicants(
    prime_implicants: list[Implicant],
    selected: list[Implicant],
    minterm_indices: list[int],
) -> list[Implicant]:
    selected_keys = {(item.pattern, tuple(item.covered_indices)) for item in selected}
    selected_cover = set()

    for item in selected:
        selected_cover.update(item.covered_indices)

    redundant: list[Implicant] = []
    minterm_set = set(minterm_indices)

    for item in prime_implicants:
        key = (item.pattern, tuple(item.covered_indices))
        if key in selected_keys:
            continue

        item_cover = set(item.covered_indices) & minterm_set
        if item_cover.issubset(selected_cover):
            redundant.append(item)

    return redundant