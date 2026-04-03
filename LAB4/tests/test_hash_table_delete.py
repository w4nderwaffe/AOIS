import pytest

from src.core.hash_table import HashTable
from src.exceptions import RecordNotFoundError
from src.models.hash_record import HashRecord


def test_delete_single_record_makes_slot_free() -> None:
    table = HashTable(size=20)
    index = table.insert(HashRecord(key="электрон", value="частица"))

    table.delete("электрон")

    entry = table._entries[index]
    assert entry.occupied is False
    assert entry.deleted is True
    assert table.active_count() == 0


def test_delete_tail_of_chain_updates_previous_terminal_flag() -> None:
    table = HashTable(size=20)
    first = table.insert(HashRecord(key="магнит", value="1"))
    second = table.insert(HashRecord(key="магнетизм", value="2"))

    table.delete("магнетизм")

    first_entry = table._entries[first]
    second_entry = table._entries[second]

    assert first_entry.terminal is True
    assert first_entry.next_index == first
    assert second_entry.occupied is False
    assert second_entry.deleted is True


def test_delete_head_of_chain_copies_next_entry_to_home_slot() -> None:
    table = HashTable(size=20)
    home_index = table.insert(HashRecord(key="магнит", value="1"))
    second_index = table.insert(HashRecord(key="магнетизм", value="2"))

    table.delete("магнит")

    home_entry = table._entries[home_index]
    moved_entry = table._entries[second_index]

    assert home_entry.key == "МАГНЕТИЗМ"
    assert home_entry.value == "2"
    assert home_entry.occupied is True
    assert moved_entry.occupied is False
    assert moved_entry.deleted is True


def test_delete_middle_entry_relinks_chain_by_copying_next() -> None:
    table = HashTable(size=20)
    table.insert(HashRecord(key="магнит", value="1"))
    middle_index = table.insert(HashRecord(key="магнетизм", value="2"))
    tail_index = table.insert(HashRecord(key="материя", value="3"))

    table.delete("магнетизм")

    middle_entry = table._entries[middle_index]
    tail_entry = table._entries[tail_index]

    assert middle_entry.key == "МАТЕРИЯ"
    assert middle_entry.value == "3"
    assert middle_entry.occupied is True
    assert tail_entry.occupied is False
    assert tail_entry.deleted is True


def test_delete_raises_for_missing_key() -> None:
    table = HashTable(size=20)

    with pytest.raises(RecordNotFoundError):
        table.delete("магнит")


def test_deleted_record_cannot_be_found() -> None:
    table = HashTable(size=20)
    table.insert(HashRecord(key="электрон", value="1"))

    table.delete("электрон")

    with pytest.raises(RecordNotFoundError):
        table.search("электрон")