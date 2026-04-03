from src.constants import ALPHABET_BASE, MIN_KEY_LENGTH, RUSSIAN_ALPHABET
from src.exceptions import InvalidKeyError


class AlphabetMapper:
    def __init__(self, alphabet: str = RUSSIAN_ALPHABET) -> None:
        self._alphabet = alphabet
        self._index_by_char = {char: index for index, char in enumerate(alphabet)}

    def normalize_key(self, key: str) -> str:
        normalized = key.strip().upper()

        if len(normalized) < MIN_KEY_LENGTH:
            raise InvalidKeyError("Ключ должен содержать минимум 2 символа.")

        for char in normalized[:2]:
            if char not in self._index_by_char:
                raise InvalidKeyError(
                    "Ключ должен начинаться минимум с двух русских букв."
                )

        return normalized

    def char_to_index(self, char: str) -> int:
        upper_char = char.upper()

        if upper_char not in self._index_by_char:
            raise InvalidKeyError(f"Символ '{char}' отсутствует в русском алфавите.")

        return self._index_by_char[upper_char]

    def compute_value(self, key: str) -> int:
        normalized = self.normalize_key(key)
        first = self.char_to_index(normalized[0])
        second = self.char_to_index(normalized[1])
        return first * ALPHABET_BASE + second