from src.exceptions import HashTableError


class LinearProbingStrategy:
    def probe(self, start_index: int, step: int, size: int) -> int:
        if size <= 0:
            raise HashTableError("Размер таблицы должен быть положительным.")

        return (start_index + step) % size