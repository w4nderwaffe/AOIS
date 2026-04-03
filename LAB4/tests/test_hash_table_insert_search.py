import pytest

from src.core.hash_table import HashTable
from src.exceptions import DuplicateKeyError, RecordNotFoundError, TableOverflowError
from src.models.hash_record import HashRecord


def test_insert_record_without_collision() -> None:
    table = HashTable(size=20)

    index = table.insert(HashRecord(key="магнит", value="данные"))

    assert index == table.compute_hash("магнит")
    assert table.active_count() == 1
    assert table.contains("магнит") is True


def test_insert_records_with_collision_builds_chain() -> None:
    table = HashTable(size=20)

    first_index = table.insert(HashRecord(key="магнит", value="1"))
    second_index = table.insert(HashRecord(key="магнетизм", value="2"))
    third_index = table.insert(HashRecord(key="материя", value="3"))

    assert first_index == table.compute_hash("магнит")
    assert second_index != first_index
    assert third_index != first_index

    first_entry = table._entries[first_index]
    second_entry = table._entries[second_index]
    third_entry = table._entries[third_index]

    assert first_entry.collision is True
    assert first_entry.terminal is False
    assert second_entry.terminal is False
    assert third_entry.terminal is True


def test_search_returns_inserted_record() -> None:
    table = HashTable(size=20)
    table.insert(HashRecord(key="магнит", value="магнитное поле"))

    record = table.search("магнит")

    assert record.key == "МАГНИТ"
    assert record.value == "магнитное поле"


def test_search_raises_for_missing_record() -> None:
    table = HashTable(size=20)

    with pytest.raises(RecordNotFoundError):
        table.search("магнит")


def test_insert_duplicate_key_raises() -> None:
    table = HashTable(size=20)
    table.insert(HashRecord(key="магнит", value="1"))

    with pytest.raises(DuplicateKeyError):
        table.insert(HashRecord(key="магнит", value="2"))


def test_find_index_returns_real_index_in_chain() -> None:
    table = HashTable(size=20)
    table.insert(HashRecord(key="магнит", value="1"))
    index = table.insert(HashRecord(key="магнетизм", value="2"))

    assert table.find_index("магнетизм") == index


def test_contains_returns_false_for_absent_key() -> None:
    table = HashTable(size=20)

    assert table.contains("магнит") is False


def test_load_factor_is_computed_correctly() -> None:
    table = HashTable(size=20)
    table.insert(HashRecord(key="магнит", value="1"))
    table.insert(HashRecord(key="температура", value="2"))

    assert table.load_factor() == 2 / 20


def test_collision_count_detects_home_entries_with_collision_flag() -> None:
    table = HashTable(size=20)
    table.insert(HashRecord(key="магнит", value="1"))
    table.insert(HashRecord(key="магнетизм", value="2"))

    assert table.collision_count() == 1


def test_chain_count_detects_number_of_home_collision_chains() -> None:
    table = HashTable(size=20)
    table.insert(HashRecord(key="магнит", value="1"))
    table.insert(HashRecord(key="магнетизм", value="2"))
    table.insert(HashRecord(key="температура", value="3"))
    table.insert(HashRecord(key="теплота", value="4"))

    assert table.chain_count() == 2


def test_build_inserts_all_records() -> None:
    table = HashTable(size=20)
    records = [
        HashRecord(key="магнит", value="1"),
        HashRecord(key="температура", value="2"),
        HashRecord(key="электрон", value="3"),
    ]

    table.build(records)

    assert table.active_count() == 3
    assert table.contains("магнит") is True
    assert table.contains("температура") is True
    assert table.contains("электрон") is True


def test_find_free_slot_raises_when_table_is_full() -> None:
    table = HashTable(size=3)
    table.insert(HashRecord(key="магнит", value="1"))
    table.insert(HashRecord(key="магнетизм", value="2"))
    table.insert(HashRecord(key="материя", value="3"))

    with pytest.raises(TableOverflowError):
        table.insert(HashRecord(key="температура", value="4"))