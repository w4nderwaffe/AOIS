from dataclasses import dataclass

from src.constants import EMPTY_NEXT_INDEX


@dataclass(slots=True)
class HashEntry:
    key: str = ""
    value: str = ""
    collision: bool = False
    occupied: bool = False
    terminal: bool = False
    linked: bool = False
    deleted: bool = False
    next_index: int = EMPTY_NEXT_INDEX

    def clear(self) -> None:
        self.key = ""
        self.value = ""
        self.collision = False
        self.occupied = False
        self.terminal = False
        self.linked = False
        self.deleted = False
        self.next_index = EMPTY_NEXT_INDEX

    def copy_from(self, other: "HashEntry") -> None:
        self.key = other.key
        self.value = other.value
        self.collision = other.collision
        self.occupied = other.occupied
        self.terminal = other.terminal
        self.linked = other.linked
        self.deleted = other.deleted
        self.next_index = other.next_index

    def is_available(self) -> bool:
        return not self.occupied

    def is_active(self) -> bool:
        return self.occupied and not self.deleted