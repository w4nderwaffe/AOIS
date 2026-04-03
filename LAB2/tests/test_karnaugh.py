from karnaugh import (
    build_karnaugh_map,
    find_karnaugh_groups,
    gray_code,
    karnaugh_cell_indices,
    minimize_by_karnaugh,
)
from lexer import Lexer
from parser import Parser
from truth_table import build_truth_table


def parse_table(text: str):
    return build_truth_table(Parser(Lexer(text).tokenize()).parse())


def test_gray_code():
    assert gray_code(0) == [""]
    assert gray_code(1) == ["0", "1"]
    assert gray_code(2) == ["00", "01", "11", "10"]


def test_karnaugh_cell_indices_for_three_vars():
    table = parse_table("(!a&b)|c")
    assert karnaugh_cell_indices(table) == [
        [0, 1, 3, 2],
        [4, 5, 7, 6],
    ]


def test_build_karnaugh_map():
    table = parse_table("(!a&b)|c")
    assert build_karnaugh_map(table) == [
        [0, 1, 1, 1],
        [0, 1, 1, 0],
    ]


def test_find_karnaugh_groups_and_minimize():
    table = parse_table("(!a&b)|c")
    groups = find_karnaugh_groups(table)
    patterns = sorted(group.pattern for group in groups)
    assert patterns == ["01X", "XX1"]

    result = minimize_by_karnaugh(table)
    assert result.minimized_expression in {"c|(!a&b)", "(!a&b)|c"}


def test_karnaugh_zero_and_one():
    zero_table = parse_table("a&!a")
    zero_result = minimize_by_karnaugh(zero_table)
    assert zero_result.minimized_expression == "0"

    one_table = parse_table("a|!a")
    one_result = minimize_by_karnaugh(one_table)
    assert one_result.minimized_expression == "1"