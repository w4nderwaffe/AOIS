import pytest

from src.core.alphabet_mapper import AlphabetMapper
from src.constants import ALPHABET_BASE
from src.exceptions import InvalidKeyError


def test_normalize_key_strips_spaces_and_uppercases() -> None:
    mapper = AlphabetMapper()

    assert mapper.normalize_key("  магнит ") == "МАГНИТ"


def test_normalize_key_raises_for_short_key() -> None:
    mapper = AlphabetMapper()

    with pytest.raises(InvalidKeyError):
        mapper.normalize_key("А")


def test_normalize_key_raises_for_non_russian_first_two_letters() -> None:
    mapper = AlphabetMapper()

    with pytest.raises(InvalidKeyError):
        mapper.normalize_key("A1том")


def test_char_to_index_returns_correct_index() -> None:
    mapper = AlphabetMapper()

    assert mapper.char_to_index("А") == 0
    assert mapper.char_to_index("Б") == 1
    assert mapper.char_to_index("Я") == 32


def test_char_to_index_raises_for_unknown_symbol() -> None:
    mapper = AlphabetMapper()

    with pytest.raises(InvalidKeyError):
        mapper.char_to_index("@")


def test_compute_value_uses_first_two_letters() -> None:
    mapper = AlphabetMapper()

    expected = mapper.char_to_index("М") * ALPHABET_BASE + mapper.char_to_index("А")

    assert mapper.compute_value("магнит") == expected


def test_compute_value_same_for_words_with_same_first_two_letters() -> None:
    mapper = AlphabetMapper()

    assert mapper.compute_value("магнит") == mapper.compute_value("магнетизм")


def test_compute_value_accepts_lowercase_letters() -> None:
    mapper = AlphabetMapper()

    assert mapper.compute_value("температура") >= 0