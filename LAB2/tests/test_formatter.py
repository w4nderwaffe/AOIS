from formatter import (
    format_analysis_result,
    format_derivative,
    format_karnaugh_result,
    format_minimization_result,
    format_numeric_forms,
    format_post_classes,
    format_truth_table,
)
from lexer import Lexer
from parser import Parser
from truth_table import build_truth_table
from app import LogicFunctionAnalyzer


def parse_table(text: str):
    return build_truth_table(Parser(Lexer(text).tokenize()).parse())


def test_format_truth_table():
    table = parse_table("(!a&b)|c")
    formatted = format_truth_table(table)
    assert "Таблица истинности:" in formatted
    assert "(!a&b)" in formatted
    assert "((!a&b)|c)" in formatted


def test_format_numeric_and_post_classes():
    analyzer = LogicFunctionAnalyzer()
    result = analyzer.analyze("(!a&b)|c")

    numeric_text = format_numeric_forms(result.numeric_forms)
    assert "Σ(1, 2, 3, 5, 7)" in numeric_text
    assert "Π(0, 4, 6)" in numeric_text

    post_text = format_post_classes(result.post_classes)
    assert "T0: Да" in post_text
    assert "T1: Да" in post_text


def test_format_derivative_and_minimizations():
    analyzer = LogicFunctionAnalyzer()
    result = analyzer.analyze("(!a&b)|c")

    derivative_text = format_derivative(result.derivatives[0])
    assert "Производная по переменным" in derivative_text

    calc_text = format_minimization_result(result.calculation_minimization)
    assert "Исходное выражение" in calc_text
    assert "Минимизированное выражение" in calc_text

    karnaugh_text = format_karnaugh_result(result.karnaugh_minimization)
    assert "Карта Карно" in karnaugh_text
    assert "Группы:" in karnaugh_text


def test_format_analysis_result():
    analyzer = LogicFunctionAnalyzer()
    result = analyzer.analyze("(!a&b)|c")
    text = format_analysis_result(result)

    assert "Результат анализа логической функции" in text
    assert "СДНФ:" in text
    assert "СКНФ:" in text
    assert "Полином Жегалкина:" in text