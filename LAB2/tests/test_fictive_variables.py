import pytest

from fictive_variables import find_fictive_variables, is_variable_fictive
from lexer import Lexer
from parser import Parser
from truth_table import build_truth_table


def parse_table(text: str):
    return build_truth_table(Parser(Lexer(text).tokenize()).parse())


def test_find_fictive_variables():
    table = parse_table("a")
    assert find_fictive_variables(table) == []
    assert is_variable_fictive(table, "a") is False


def test_find_fictive_variables_for_tautology():
    table = parse_table("a|!a")
    assert find_fictive_variables(table) == ["a"]


def test_variable_absent_error():
    table = parse_table("a")
    with pytest.raises(ValueError):
        is_variable_fictive(table, "b")