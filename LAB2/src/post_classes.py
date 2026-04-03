from models import PostClassesResult, TruthTable
from zhegalkin import build_zhegalkin_terms


def check_t0(table: TruthTable) -> bool:
    return table.rows[0].result == 0


def check_t1(table: TruthTable) -> bool:
    return table.rows[-1].result == 1


def check_self_dual(table: TruthTable) -> bool:
    size = len(table.rows)
    results = table.results_vector()

    for index in range(size):
        opposite = size - 1 - index
        if results[index] == results[opposite]:
            return False

    return True


def _tuple_from_row(table: TruthTable, index: int) -> tuple[int, ...]:
    row = table.rows[index]
    return tuple(row.values[variable] for variable in table.variables)


def _less_or_equal(left: tuple[int, ...], right: tuple[int, ...]) -> bool:
    for left_value, right_value in zip(left, right):
        if left_value > right_value:
            return False
    return True


def check_monotone(table: TruthTable) -> bool:
    tuples = [_tuple_from_row(table, index) for index in range(len(table.rows))]
    results = table.results_vector()

    for left_index, left_tuple in enumerate(tuples):
        for right_index, right_tuple in enumerate(tuples):
            if _less_or_equal(left_tuple, right_tuple):
                if results[left_index] > results[right_index]:
                    return False

    return True


def check_linear(table: TruthTable) -> bool:
    terms = build_zhegalkin_terms(table)

    for term in terms:
        if len(term.variables) > 1:
            return False

    return True


def analyze_post_classes(table: TruthTable) -> PostClassesResult:
    return PostClassesResult(
        t0=check_t0(table),
        t1=check_t1(table),
        s=check_self_dual(table),
        m=check_monotone(table),
        l=check_linear(table),
    )