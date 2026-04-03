from lexer import Lexer
from parser import Parser
from post_classes import (
    analyze_post_classes,
    check_linear,
    check_monotone,
    check_self_dual,
    check_t0,
    check_t1,
)
from truth_table import build_truth_table


def parse_table(text: str):
    return build_truth_table(Parser(Lexer(text).tokenize()).parse())


def test_post_classes_for_and():
    table = parse_table("a&b")
    result = analyze_post_classes(table)

    assert check_t0(table) is True
    assert check_t1(table) is True
    assert check_self_dual(table) is False
    assert check_monotone(table) is True
    assert check_linear(table) is False

    assert result.t0 is True
    assert result.t1 is True
    assert result.s is False
    assert result.m is True
    assert result.l is False


def test_post_classes_for_xor_like_equivalence_negated():
    table = parse_table("!(a~b)")
    assert check_linear(table) is True


def test_post_classes_for_not_a():
    table = parse_table("!a")
    assert check_self_dual(table) is True
    assert check_t0(table) is False
    assert check_t1(table) is False
    assert check_monotone(table) is False