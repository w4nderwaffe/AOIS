from src.constants import BASE_ADDRESS, EMPTY_NEXT_INDEX, TABLE_SIZE
from src.core.alphabet_mapper import AlphabetMapper
from src.core.hash_function import HashFunction
from src.core.probing import LinearProbingStrategy
from src.exceptions import DuplicateKeyError, RecordNotFoundError, TableOverflowError
from src.models.hash_entry import HashEntry
from src.models.hash_record import HashRecord


class HashTable:
    def __init__(
        self,
        size: int = TABLE_SIZE,
        base_address: int = BASE_ADDRESS,
        mapper: AlphabetMapper | None = None,
        hash_function: HashFunction | None = None,
        probing: LinearProbingStrategy | None = None,
    ) -> None:
        self._size = size
        self._base_address = base_address
        self._mapper = mapper or AlphabetMapper()
        self._hash_function = hash_function or HashFunction()
        self._probing = probing or LinearProbingStrategy()
        self._entries = [HashEntry() for _ in range(size)]

    @property
    def size(self) -> int:
        return self._size

    @property
    def base_address(self) -> int:
        return self._base_address

    def compute_value(self, key: str) -> int:
        return self._mapper.compute_value(key)

    def compute_hash(self, key: str) -> int:
        value = self.compute_value(key)
        return self._hash_function.compute(value, self._size, self._base_address)

    def build(self, records: list[HashRecord]) -> None:
        for record in records:
            self.insert(record)

    def insert(self, record: HashRecord) -> int:
        key = self._mapper.normalize_key(record.key)
        if self.contains(key):
            raise DuplicateKeyError(f"Ключ '{record.key}' уже существует в таблице.")

        home_index = self.compute_hash(key)
        home_entry = self._entries[home_index]

        if not home_entry.occupied:
            self._write_entry(
                index=home_index,
                key=key,
                value=record.value,
                collision=False,
                terminal=True,
                next_index=home_index,
            )
            return home_index

        free_index = self._find_free_slot(home_index)
        tail_index = self._find_tail_index(home_index)

        self._write_entry(
            index=free_index,
            key=key,
            value=record.value,
            collision=False,
            terminal=True,
            next_index=home_index,
        )

        home_entry.collision = True

        tail_entry = self._entries[tail_index]
        tail_entry.terminal = False
        tail_entry.next_index = free_index

        return free_index

    def search(self, key: str) -> HashRecord:
        index = self.find_index(key)
        entry = self._entries[index]
        return HashRecord(key=entry.key, value=entry.value)

    def find_index(self, key: str) -> int:
        normalized = self._mapper.normalize_key(key)
        home_index = self.compute_hash(normalized)

        for index in self._iter_chain_indices(home_index):
            entry = self._entries[index]
            if entry.occupied and entry.key == normalized:
                return index

        raise RecordNotFoundError(f"Ключ '{key}' не найден.")

    def contains(self, key: str) -> bool:
        try:
            self.find_index(key)
        except RecordNotFoundError:
            return False
        return True

    def delete(self, key: str) -> None:
        normalized = self._mapper.normalize_key(key)
        home_index = self.compute_hash(normalized)
        delete_index = self.find_index(normalized)
        entry = self._entries[delete_index]

        if entry.terminal and entry.next_index == delete_index:
            self._mark_deleted(delete_index)
            return

        if entry.terminal:
            previous_index = self._find_previous_index(home_index, delete_index)
            self._mark_deleted(delete_index)
            previous_entry = self._entries[previous_index]
            previous_entry.terminal = True
            previous_entry.next_index = home_index
            return

        if entry.collision:
            next_index = entry.next_index
            self._copy_entry(next_index, delete_index, collision=True)
            self._mark_deleted(next_index)
            return

        next_index = entry.next_index
        self._copy_entry(next_index, delete_index, collision=False)
        self._mark_deleted(next_index)

    def active_count(self) -> int:
        return sum(1 for entry in self._entries if entry.occupied)

    def load_factor(self) -> float:
        return self.active_count() / self._size

    def collision_count(self) -> int:
        return sum(1 for entry in self._entries if entry.occupied and entry.collision)

    def chain_count(self) -> int:
        count = 0
        for index, entry in enumerate(self._entries):
            if not entry.occupied:
                continue
            if self.compute_hash(entry.key) == index and entry.collision:
                count += 1
        return count

    def to_rows(self) -> list[dict[str, object]]:
        rows = []
        for index, entry in enumerate(self._entries):
            value = self.compute_value(entry.key) if entry.occupied else None
            hash_index = self.compute_hash(entry.key) if entry.occupied else None
            rows.append(
                {
                    "index": index,
                    "key": entry.key,
                    "collision": entry.collision,
                    "occupied": entry.occupied,
                    "terminal": entry.terminal,
                    "linked": entry.linked,
                    "deleted": entry.deleted,
                    "next_index": entry.next_index,
                    "value": entry.value,
                    "v": value,
                    "h": hash_index,
                }
            )
        return rows

    def _write_entry(
        self,
        index: int,
        key: str,
        value: str,
        collision: bool,
        terminal: bool,
        next_index: int,
    ) -> None:
        entry = self._entries[index]
        entry.key = key
        entry.value = value
        entry.collision = collision
        entry.occupied = True
        entry.terminal = terminal
        entry.linked = False
        entry.deleted = False
        entry.next_index = next_index

    def _mark_deleted(self, index: int) -> None:
        entry = self._entries[index]
        entry.key = ""
        entry.value = ""
        entry.collision = False
        entry.occupied = False
        entry.terminal = False
        entry.linked = False
        entry.deleted = True
        entry.next_index = EMPTY_NEXT_INDEX

    def _copy_entry(self, source_index: int, target_index: int, collision: bool) -> None:
        source = self._entries[source_index]
        target = self._entries[target_index]

        target.key = source.key
        target.value = source.value
        target.collision = collision
        target.occupied = source.occupied
        target.terminal = source.terminal
        target.linked = source.linked
        target.deleted = False
        target.next_index = source.next_index

    def _find_free_slot(self, start_index: int) -> int:
        for step in range(1, self._size + 1):
            index = self._probing.probe(start_index, step, self._size)
            if not self._entries[index].occupied:
                return index
        raise TableOverflowError("В таблице нет свободных ячеек.")

    def _find_tail_index(self, home_index: int) -> int:
        current_index = home_index

        while True:
            entry = self._entries[current_index]
            if entry.terminal:
                return current_index
            current_index = entry.next_index

    def _find_previous_index(self, home_index: int, target_index: int) -> int:
        current_index = home_index

        while True:
            entry = self._entries[current_index]
            if entry.terminal:
                break
            if entry.next_index == target_index:
                return current_index
            current_index = entry.next_index

        raise RecordNotFoundError("Предыдущий элемент цепочки не найден.")

    def _iter_chain_indices(self, home_index: int):
        visited = set()
        current_index = home_index

        while current_index not in visited:
            visited.add(current_index)
            entry = self._entries[current_index]

            if not entry.occupied:
                return

            yield current_index

            if entry.terminal:
                return

            current_index = entry.next_index