from app import LogicFunctionAnalyzer
import main


def test_app_analyze():
    analyzer = LogicFunctionAnalyzer()
    result = analyzer.analyze("(!a&b)|c")

    assert result.expression == "(!a&b)|c"
    assert result.variables == ["a", "b", "c"]
    assert result.sdnf == "(!a&!b&c)|(!a&b&!c)|(!a&b&c)|(a&!b&c)|(a&b&c)"
    assert result.sknf == "(a|b|c)&(!a|b|c)&(!a|!b|c)"
    assert result.calculation_minimization.minimized_expression == "(!a&b)|c"


def test_app_empty_expression():
    analyzer = LogicFunctionAnalyzer()
    try:
        analyzer.analyze("   ")
        assert False
    except ValueError as error:
        assert str(error) == "Пустое выражение"


def test_read_expression(monkeypatch):
    inputs = iter(["", "   ", "a&b"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    assert main.read_expression() == "a&b"


def test_choose_derivative_empty(capsys):
    class Dummy:
        derivatives = []

    main.choose_derivative(Dummy())
    output = capsys.readouterr().out
    assert "Производные отсутствуют." in output


def test_choose_derivative_select(monkeypatch, capsys):
    analyzer = LogicFunctionAnalyzer()
    result = analyzer.analyze("a|b")
    inputs = iter(["100", "x", "1"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    main.choose_derivative(result)
    output = capsys.readouterr().out
    assert "Такого номера нет." in output
    assert "Введите корректный номер." in output
    assert "Производная по переменным" in output


def test_print_full_analysis(capsys):
    analyzer = LogicFunctionAnalyzer()
    result = analyzer.analyze("a|b")
    main.print_full_analysis(result)
    output = capsys.readouterr().out
    assert "Исходное выражение:" in output
    assert "Минимизация расчетным методом:" in output


def test_main_menu_flow(monkeypatch, capsys):
    inputs = iter([
        "(!a&b)|c",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "1",
        "10",
        "11",
        "12",
        "13",
        "1",
        "a|b",
        "0",
    ])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    main.main()
    output = capsys.readouterr().out

    assert "Функция успешно разобрана." in output
    assert "Таблица истинности:" in output
    assert "СДНФ:" in output
    assert "СКНФ:" in output
    assert "Числовые формы:" in output
    assert "Классы Поста:" in output
    assert "Полином Жегалкина:" in output
    assert "Фиктивные переменные:" in output
    assert "Минимизация расчетным методом:" in output
    assert "Минимизация расчетно-табличным методом:" in output
    assert "Минимизация табличным методом (карта Карно):" in output
    assert "Завершение программы." in output