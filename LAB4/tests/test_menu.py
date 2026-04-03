from src.core.hash_table import HashTable
from src.menu import Menu
from src.models.hash_record import HashRecord


def test_menu_run_exit_branch(monkeypatch, capsys) -> None:
    table = HashTable()
    menu = Menu(table)

    inputs = iter(["0"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    menu.run()

    output = capsys.readouterr().out
    assert "Завершение программы." in output


def test_menu_run_invalid_choice_branch(monkeypatch, capsys) -> None:
    table = HashTable()
    menu = Menu(table)

    inputs = iter(["9", "0"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    menu.run()

    output = capsys.readouterr().out
    assert "Некорректный пункт меню." in output
    assert "Завершение программы." in output


def test_menu_show_table_branch(monkeypatch, capsys) -> None:
    table = HashTable()
    table.insert(HashRecord(key="магнит", value="поле"))
    menu = Menu(table)

    inputs = iter(["1", "0"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    menu.run()

    output = capsys.readouterr().out
    assert "Размер таблицы" in output
    assert "МАГНИТ" in output


def test_menu_show_summary_branch(monkeypatch, capsys) -> None:
    table = HashTable()
    table.insert(HashRecord(key="магнит", value="поле"))
    menu = Menu(table)

    inputs = iter(["5", "0"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    menu.run()

    output = capsys.readouterr().out
    assert "Количество активных записей" in output
    assert "Коэффициент заполнения" in output


def test_menu_search_record_success(monkeypatch, capsys) -> None:
    table = HashTable()
    table.insert(HashRecord(key="магнит", value="магнитное поле"))
    menu = Menu(table)

    inputs = iter(["2", "магнит", "0"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    menu.run()

    output = capsys.readouterr().out
    assert "Запись найдена." in output
    assert "Ключ: МАГНИТ" in output
    assert "Данные: магнитное поле" in output
    assert "V:" in output
    assert "h:" in output


def test_menu_search_record_error(monkeypatch, capsys) -> None:
    table = HashTable()
    menu = Menu(table)

    inputs = iter(["2", "магнит", "0"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    menu.run()

    output = capsys.readouterr().out
    assert "не найден" in output.lower()


def test_menu_add_record_success(monkeypatch, capsys) -> None:
    table = HashTable()
    menu = Menu(table)

    inputs = iter(["3", "магнит", "магнитное поле", "0"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    menu.run()

    output = capsys.readouterr().out
    assert "Запись добавлена в строку" in output
    assert table.contains("магнит") is True


def test_menu_add_record_duplicate_error(monkeypatch, capsys) -> None:
    table = HashTable()
    table.insert(HashRecord(key="магнит", value="1"))
    menu = Menu(table)

    inputs = iter(["3", "магнит", "2", "0"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    menu.run()

    output = capsys.readouterr().out
    assert "уже существует" in output.lower()


def test_menu_add_record_invalid_key_error(monkeypatch, capsys) -> None:
    table = HashTable()
    menu = Menu(table)

    inputs = iter(["3", "1", "данные", "0"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    menu.run()

    output = capsys.readouterr().out
    assert "минимум 2 символа" in output.lower() or "русских букв" in output.lower()


def test_menu_delete_record_success(monkeypatch, capsys) -> None:
    table = HashTable()
    table.insert(HashRecord(key="магнит", value="1"))
    menu = Menu(table)

    inputs = iter(["4", "магнит", "0"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    menu.run()

    output = capsys.readouterr().out
    assert "Запись удалена." in output
    assert table.contains("магнит") is False


def test_menu_delete_record_error(monkeypatch, capsys) -> None:
    table = HashTable()
    menu = Menu(table)

    inputs = iter(["4", "магнит", "0"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    menu.run()

    output = capsys.readouterr().out
    assert "не найден" in output.lower()