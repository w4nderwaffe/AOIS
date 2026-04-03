import pytest

from src.core.hash_function import HashFunction
from src.exceptions import HashTableError


def test_compute_hash_returns_modulo_with_zero_base() -> None:
    hash_function = HashFunction()

    assert hash_function.compute(75, 20, 0) == 15


def test_compute_hash_returns_modulo_with_non_zero_base() -> None:
    hash_function = HashFunction()

    assert hash_function.compute(75, 20, 5) == 20


def test_compute_hash_raises_for_non_positive_size() -> None:
    hash_function = HashFunction()

    with pytest.raises(HashTableError):
        hash_function.compute(10, 0, 0)