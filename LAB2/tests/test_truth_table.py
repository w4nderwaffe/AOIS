import pytest

from errors import TruthTableError
from lexer import Lexer
from parser import Parser
from truth_table import build_truth_table, extract_variables, generate_assignments


def parse(text: str):
    return Parser(Lexer(text).tokenize()).parse()


def test_extract_variables_sorted():
    root = parse("(c&a)|b")
    assert extract_variables(root) == ["a", "b", "c"]


def test_extract_variables_no_variables():
    class DummyNode:
        def collect_variables(self):
            return set()

    with pytest.raises(TruthTableError):
        extract_variables(DummyNode())


def test_extract_variables_too_many():
    class DummyNode:
        def collect_variables(self):
            return {"a", "b", "c", "d", "e", "f"}

    with pytest.raises(TruthTableError):
        extract_variables(DummyNode())


def test_generate_assignments():
    assignments = generate_assignments(["a", "b"])
    assert assignments == [
        {"a": 0, "b": 0},
        {"a": 0, "b": 1},
        {"a": 1, "b": 0},
        {"a": 1, "b": 1},
    ]


def test_generate_assignments_errors():
    with pytest.raises(TruthTableError):
        generate_assignments([])
    with pytest.raises(TruthTableError):
        generate_assignments(["a", "b", "c", "d", "e", "f"])


def test_build_truth_table_full_expression_columns():
    root = parse("(!a&b)|c")
    table = build_truth_table(root)

    assert table.variables == ["a", "b", "c"]
    assert table.expressions == ["!a", "(!a&b)", "((!a&b)|c)"]
    assert len(table.rows) == 8
    assert table.rows[0].result == 0
    assert table.rows[1].result == 1
    assert table.rows[2].expression_values["!a"] == 1
    assert table.rows[2].expression_values["(!a&b)"] == 1
    assert table.rows[2].expression_values["((!a&b)|c)"] == 1
    assert table.results_vector() == [0, 1, 1, 1, 0, 1, 0, 1]


def test_build_truth_table_invalid_result():
    class DummyNode:
        def collect_variables(self):
            return {"a"}

        def collect_subexpressions(self):
            return []

        def fill_expression_values(self, values, target):
            return 5

    with pytest.raises(TruthTableError):
        build_truth_table(DummyNode())


def test_build_truth_table_missing_expression_value():
    class DummyNode:
        def collect_variables(self):
            return {"a"}

        def collect_subexpressions(self):
            return ["x"]

        def fill_expression_values(self, values, target):
            return 1

    with pytest.raises(TruthTableError):
        build_truth_table(DummyNode())