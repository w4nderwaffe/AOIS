import pytest

from src.core.probing import LinearProbingStrategy
from src.exceptions import HashTableError


def test_probe_moves_linearly() -> None:
    probing = LinearProbingStrategy()

    assert probing.probe(5, 1, 20) == 6
    assert probing.probe(5, 2, 20) == 7


def test_probe_wraps_around_table() -> None:
    probing = LinearProbingStrategy()

    assert probing.probe(19, 1, 20) == 0
    assert probing.probe(19, 3, 20) == 2


def test_probe_raises_for_non_positive_size() -> None:
    probing = LinearProbingStrategy()

    with pytest.raises(HashTableError):
        probing.probe(0, 1, 0)