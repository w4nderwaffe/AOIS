from lexer import Lexer
from parser import Parser
from truth_table import build_truth_table
from zhegalkin import (
    build_difference_triangle,
    build_zhegalkin_polynomial,
    build_zhegalkin_terms,
    coefficient_index_to_variables,
    extract_zhegalkin_coefficients,
    format_zhegalkin_polynomial,
)


def parse_table(text: str):
    return build_truth_table(Parser(Lexer(text).tokenize()).parse())


def test_difference_triangle_and_coefficients():
    values = [0, 1, 1, 0]
    triangle = build_difference_triangle(values)
    assert triangle == [
        [0, 1, 1, 0],
        [1, 0, 1],
        [1, 1],
        [0],
    ]
    assert extract_zhegalkin_coefficients(values) == [0, 1, 1, 0]


def test_coefficient_index_to_variables():
    assert coefficient_index_to_variables(0, ["a", "b", "c"]) == []
    assert coefficient_index_to_variables(5, ["a", "b", "c"]) == ["a", "c"]


def test_zhegalkin_for_or():
    table = parse_table("a|b")
    terms = build_zhegalkin_terms(table)
    polynomial = format_zhegalkin_polynomial(terms)
    assert polynomial == "b ⊕ a ⊕ a*b"
    assert build_zhegalkin_polynomial(table) == "b ⊕ a ⊕ a*b"


def test_zhegalkin_zero():
    assert format_zhegalkin_polynomial([]) == "0"