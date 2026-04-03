from src.core.hash_table import HashTable
from src.models.hash_record import HashRecord
from src.presenters.table_formatter import TableFormatter


def test_format_table_contains_header_and_record() -> None:
    table = HashTable(size=20)
    table.insert(HashRecord(key="магнит", value="магнитное поле"))

    result = TableFormatter.format_table(table)

    assert "ID" in result
    assert "Pi" in result
    assert "МАГНИТ" in result
    assert "магнитное поле" in result


def test_format_summary_contains_required_metrics() -> None:
    table = HashTable(size=20)
    table.insert(HashRecord(key="магнит", value="1"))

    result = TableFormatter.format_summary(table)

    assert "Размер таблицы" in result
    assert "Количество активных записей: 1" in result
    assert "Коэффициент заполнения: 0.05" in result


def test_format_full_report_combines_summary_and_table() -> None:
    table = HashTable(size=20)
    table.insert(HashRecord(key="магнит", value="1"))

    result = TableFormatter.format_full_report(table)

    assert "Размер таблицы" in result
    assert "ID" in result
    assert "МАГНИТ" in result