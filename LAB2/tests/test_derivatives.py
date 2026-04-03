import pytest

from derivatives import (
    build_all_required_derivatives,
    build_derivative_expression,
    build_derivative_truth_table,
    build_mixed_derivative,
    build_partial_derivative,
    flip_variables,
)
from lexer import Lexer
from parser import Parser


def parse(text: str):
    return Parser(Lexer(text).tokenize()).parse()


def test_flip_variables():
    assert flip_variables({"a": 0, "b": 1}, ["a", "b"]) == {"a": 1, "b": 0}


def test_flip_variables_error():
    with pytest.raises(ValueError):
        flip_variables({"a": 0}, ["b"])


def test_partial_derivative_for_or():
    root = parse("a|b")
    derivative = build_partial_derivative(root, ["a", "b"], "a")
    assert derivative.by_variables == ["a"]
    assert derivative.truth_table.results_vector() == [1, 0, 1, 0]
    assert derivative.expression == "(!a&!b)|(a&!b)"


def test_mixed_derivative_for_or():
    root = parse("a|b")
    derivative = build_mixed_derivative(root, ["a", "b"], ["a", "b"])
    assert derivative.by_variables == ["a", "b"]
    assert derivative.truth_table.results_vector() == [1, 1, 1, 1]
    assert derivative.expression == "(!a&!b)|(!a&b)|(a&!b)|(a&b)"


def test_derivative_truth_table_structure():
    root = parse("(!a&b)|c")
    table = build_derivative_truth_table(root, ["a", "b", "c"], ["a"])
    assert table.expressions == ["D[a]"]
    assert len(table.rows) == 8
    assert all("D[a]" in row.expression_values for row in table.rows)


def test_build_derivative_expression():
    root = parse("a")
    table = build_derivative_truth_table(root, ["a"], ["a"])
    assert build_derivative_expression(table) == "!a|a"


def test_partial_derivative_invalid_variable():
    with pytest.raises(ValueError):
        build_partial_derivative(parse("a|b"), ["a", "b"], "c")


def test_mixed_derivative_invalid_variable():
    with pytest.raises(ValueError):
        build_mixed_derivative(parse("a|b"), ["a", "b"], ["a", "c"])


def test_build_all_required_derivatives():
    root = parse("a|b|c")
    derivatives = build_all_required_derivatives(root, ["a", "b", "c"])
    assert len(derivatives) == 7