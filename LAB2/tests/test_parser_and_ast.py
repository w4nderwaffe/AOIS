import pytest

from ast_nodes import AndNode, EqNode, ImplNode, NotNode, OrNode, VariableNode
from errors import ParserError
from lexer import Lexer
from parser import Parser


def parse(text: str):
    return Parser(Lexer(text).tokenize()).parse()


def test_parse_variable():
    root = parse("a")
    assert isinstance(root, VariableNode)
    assert root.to_expression() == "a"


def test_parse_not_and_collect_variables():
    root = parse("!a")
    assert isinstance(root, NotNode)
    assert root.collect_variables() == {"a"}
    assert root.to_expression() == "!a"


def test_parse_and_precedence_over_or():
    root = parse("a|b&c")
    assert isinstance(root, OrNode)
    assert root.to_expression() == "(a|(b&c))"


def test_parse_implication_right_associative():
    root = parse("a->b->c")
    assert isinstance(root, ImplNode)
    assert root.to_expression() == "(a->(b->c))"


def test_parse_equivalence():
    root = parse("a~b")
    assert isinstance(root, EqNode)
    assert root.to_expression() == "(a~b)"


def test_parse_parentheses():
    root = parse("(a|b)&c")
    assert isinstance(root, AndNode)
    assert root.to_expression() == "((a|b)&c)"


def test_parse_unexpected_end():
    with pytest.raises(ParserError):
        parse("a&")


def test_parse_extra_token():
    with pytest.raises(ParserError):
        parse("a)b")


def test_parse_empty_tokens():
    with pytest.raises(ParserError):
        Parser([]).parse()


def test_parse_primary_unexpected_token():
    parser = Parser(Lexer(")").tokenize())
    with pytest.raises(ParserError):
        parser.parse()


def test_variable_node_errors():
    node = VariableNode("a")
    with pytest.raises(KeyError):
        node.evaluate({})
    with pytest.raises(ValueError):
        node.evaluate({"a": 2})


def test_ast_evaluation_all_operations():
    assert parse("a&b").evaluate({"a": 1, "b": 1}) == 1
    assert parse("a|b").evaluate({"a": 0, "b": 1}) == 1
    assert parse("a->b").evaluate({"a": 1, "b": 0}) == 0
    assert parse("a~b").evaluate({"a": 1, "b": 1}) == 1
    assert parse("!a").evaluate({"a": 0}) == 1


def test_fill_expression_values_and_collect_subexpressions():
    root = parse("(!a&b)|c")
    target = {}
    result = root.fill_expression_values({"a": 0, "b": 1, "c": 0}, target)
    assert result == 1
    assert target["!a"] == 1
    assert target["(!a&b)"] == 1
    assert target["((!a&b)|c)"] == 1
    assert root.collect_subexpressions() == ["!a", "(!a&b)", "((!a&b)|c)"]