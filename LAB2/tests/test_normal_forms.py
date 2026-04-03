from lexer import Lexer
from models import NumericForms
from normal_forms import (
    build_index_form,
    build_numeric_forms,
    build_sdnf,
    build_sdnf_terms,
    build_sknf,
    build_sknf_terms,
)
from parser import Parser
from truth_table import build_truth_table


def parse_table(text: str):
    return build_truth_table(Parser(Lexer(text).tokenize()).parse())


def test_normal_forms_for_expression():
    table = parse_table("(!a&b)|c")

    assert build_sdnf_terms(table) == [
        "(!a&!b&c)",
        "(!a&b&!c)",
        "(!a&b&c)",
        "(a&!b&c)",
        "(a&b&c)",
    ]
    assert build_sknf_terms(table) == [
        "(a|b|c)",
        "(!a|b|c)",
        "(!a|!b|c)",
    ]
    assert build_sdnf(table) == "(!a&!b&c)|(!a&b&!c)|(!a&b&c)|(a&!b&c)|(a&b&c)"
    assert build_sknf(table) == "(a|b|c)&(!a|b|c)&(!a|!b|c)"


def test_numeric_forms_and_index():
    table = parse_table("(!a&b)|c")
    forms = build_numeric_forms(table)
    assert isinstance(forms, NumericForms)
    assert forms.sdnf_indices == [1, 2, 3, 5, 7]
    assert forms.sknf_indices == [0, 4, 6]
    assert forms.index_form == 117
    assert build_index_form(table) == 117


def test_constant_zero_forms():
    table = parse_table("a&!a")
    assert build_sdnf(table) == "0"


def test_constant_one_forms():
    table = parse_table("a|!a")
    assert build_sknf(table) == "1"