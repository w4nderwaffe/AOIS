from src.models.hash_entry import HashEntry


def test_hash_entry_clear_resets_all_fields() -> None:
    entry = HashEntry(
        key="МАГНИТ",
        value="данные",
        collision=True,
        occupied=True,
        terminal=True,
        linked=True,
        deleted=True,
        next_index=7,
    )

    entry.clear()

    assert entry.key == ""
    assert entry.value == ""
    assert entry.collision is False
    assert entry.occupied is False
    assert entry.terminal is False
    assert entry.linked is False
    assert entry.deleted is False
    assert entry.next_index == -1


def test_hash_entry_copy_from_copies_all_fields() -> None:
    source = HashEntry(
        key="ТЕПЛОТА",
        value="энергия",
        collision=True,
        occupied=True,
        terminal=False,
        linked=False,
        deleted=False,
        next_index=11,
    )
    target = HashEntry()

    target.copy_from(source)

    assert target.key == "ТЕПЛОТА"
    assert target.value == "энергия"
    assert target.collision is True
    assert target.occupied is True
    assert target.terminal is False
    assert target.linked is False
    assert target.deleted is False
    assert target.next_index == 11


def test_hash_entry_is_available_and_is_active() -> None:
    entry = HashEntry()

    assert entry.is_available() is True
    assert entry.is_active() is False

    entry.occupied = True

    assert entry.is_available() is False
    assert entry.is_active() is True

    entry.deleted = True

    assert entry.is_active() is False