import pytest

from src.core.hash_table import HashTable
from src.exceptions import RecordNotFoundError
from src.models.hash_record import HashRecord


def test_find_previous_index_raises_when_previous_not_found() -> None:
    table = HashTable()
    table.insert(HashRecord(key="магнит", value="1"))
    table.insert(HashRecord(key="магнетизм", value="2"))

    home_index = table.compute_hash("магнит")

    with pytest.raises(RecordNotFoundError):
        table._find_previous_index(home_index, 999)


def test_iter_chain_indices_stops_on_empty_home_slot() -> None:
    table = HashTable()

    indices = list(table._iter_chain_indices(0))

    assert indices == []


def test_to_rows_for_empty_slot_contains_none_values() -> None:
    table = HashTable()
    rows = table.to_rows()

    assert rows[0]["v"] is None
    assert rows[0]["h"] is None


def test_delete_tail_then_search_removed_record_raises() -> None:
    table = HashTable()
    table.insert(HashRecord(key="магнит", value="1"))
    table.insert(HashRecord(key="магнетизм", value="2"))

    table.delete("магнетизм")

    with pytest.raises(RecordNotFoundError):
        table.search("магнетизм")