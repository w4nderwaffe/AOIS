import pytest

from implicants import (
    build_coverage_table,
    build_initial_implicants_from_sdnf,
    find_essential_implicants,
    find_prime_implicants,
    find_redundant_implicants,
    glue_patterns,
    minterm_index_to_pattern,
    pattern_covers_index,
    pattern_to_expression,
    patterns_differ_by_one_bit,
    remove_duplicate_implicants,
)
from lexer import Lexer
from models import Implicant
from parser import Parser
from truth_table import build_truth_table


def parse_table(text: str):
    return build_truth_table(Parser(Lexer(text).tokenize()).parse())


def test_minterm_index_to_pattern():
    assert minterm_index_to_pattern(5, 3) == "101"


def test_minterm_index_to_pattern_errors():
    with pytest.raises(ValueError):
        minterm_index_to_pattern(0, 0)
    with pytest.raises(ValueError):
        minterm_index_to_pattern(8, 3)


def test_patterns_differ_by_one_bit():
    assert patterns_differ_by_one_bit("001", "011") is True
    assert patterns_differ_by_one_bit("0X1", "011") is False


def test_patterns_differ_by_one_bit_error():
    with pytest.raises(ValueError):
        patterns_differ_by_one_bit("01", "001")


def test_glue_patterns():
    assert glue_patterns("001", "011") == "0X1"


def test_glue_patterns_error():
    with pytest.raises(ValueError):
        glue_patterns("001", "111")


def test_pattern_covers_index():
    assert pattern_covers_index("0X1", 1, 3) is True
    assert pattern_covers_index("0X1", 3, 3) is True
    assert pattern_covers_index("0X1", 5, 3) is False


def test_pattern_to_expression():
    assert pattern_to_expression("0X1", ["a", "b", "c"]) == "(!a&c)"
    assert pattern_to_expression("XXX", ["a", "b", "c"]) == "1"


def test_pattern_to_expression_error():
    with pytest.raises(ValueError):
        pattern_to_expression("01", ["a", "b", "c"])


def test_build_initial_implicants():
    table = parse_table("a|b")
    items = build_initial_implicants_from_sdnf(table)
    assert [item.pattern for item in items] == ["01", "10", "11"]


def test_remove_duplicate_implicants():
    items = [
        Implicant("01", [1]),
        Implicant("01", [1]),
        Implicant("X1", [1, 3]),
    ]
    unique = remove_duplicate_implicants(items)
    assert len(unique) == 2


def test_find_prime_implicants():
    table = parse_table("a|b")
    initial = build_initial_implicants_from_sdnf(table)
    steps, primes = find_prime_implicants(initial)

    assert len(steps) >= 1
    assert [item.pattern for item in primes] == ["1X", "X1"]


def test_build_coverage_table_and_essential_and_redundant():
    primes = [
        Implicant("1X", [2, 3]),
        Implicant("X1", [1, 3]),
        Implicant("11", [3]),
    ]
    minterms = [1, 2, 3]

    coverage = build_coverage_table(primes, minterms)
    assert coverage == [
        [0, 1, 1],
        [1, 0, 1],
        [0, 0, 1],
    ]

    essential = find_essential_implicants(primes, minterms)
    assert [item.pattern for item in essential] == ["1X", "X1"]

    redundant = find_redundant_implicants(primes, essential, minterms)
    assert [item.pattern for item in redundant] == ["11"]