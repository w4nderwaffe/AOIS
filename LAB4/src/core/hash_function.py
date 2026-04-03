from src.exceptions import HashTableError


class HashFunction:
    def compute(self, value: int, size: int, base_address: int = 0) -> int:
        if size <= 0:
            raise HashTableError("Размер таблицы должен быть положительным.")

        return value % size + base_address