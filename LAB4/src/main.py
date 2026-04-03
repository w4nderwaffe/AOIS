from src.core.hash_table import HashTable
from src.menu import Menu
from src.services.physics_dataset import get_physics_records


def build_default_table() -> HashTable:
    table = HashTable()
    table.build(get_physics_records())
    return table


def main() -> None:
    table = build_default_table()
    menu = Menu(table)
    menu.run()


if __name__ == "__main__":
    main()