from lexer import Lexer
from minimization import (
    implicants_to_expression,
    minimize_by_calculation,
    minimize_by_calculation_table,
    select_implicants_greedy,
)
from models import Implicant
from parser import Parser
from truth_table import build_truth_table


def parse_table(text: str):
    return build_truth_table(Parser(Lexer(text).tokenize()).parse())


def test_select_implicants_greedy():
    items = [
        Implicant("1X", [2, 3]),
        Implicant("X1", [1, 3]),
        Implicant("11", [3]),
    ]
    selected = select_implicants_greedy(items, [1, 2, 3])
    assert [item.pattern for item in selected] == ["1X", "X1"]


def test_implicants_to_expression():
    items = [Implicant("01X", [2, 3]), Implicant("XX1", [1, 3, 5, 7])]
    assert implicants_to_expression(items, ["a", "b", "c"]) == "(!a&b)|c"
    assert implicants_to_expression([], ["a", "b"]) == "0"


def test_minimize_by_calculation():
    table = parse_table("(!a&b)|c")
    result = minimize_by_calculation(table)

    assert result.original_expression == "(!a&!b&c)|(!a&b&!c)|(!a&b&c)|(a&!b&c)|(a&b&c)"
    assert result.minimized_expression == "(!a&b)|c"
    assert len(result.gluing_steps) == 2
    assert [item.pattern for item in result.prime_implicants] == ["01X", "XX1"]


def test_minimize_by_calculation_table():
    table = parse_table("(!a&b)|c")
    result = minimize_by_calculation_table(table)

    assert result.minimized_expression == "(!a&b)|c"
    assert result.coverage_table == [
        [0, 1, 1, 0, 0],
        [1, 0, 1, 1, 1],
    ]


def test_minimize_zero_and_one():
    zero_table = parse_table("a&!a")
    zero_result = minimize_by_calculation(zero_table)
    assert zero_result.minimized_expression == "0"

    one_table = parse_table("a|!a")
    one_result = minimize_by_calculation_table(one_table)
    assert one_result.minimized_expression == "1"