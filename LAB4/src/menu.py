from src.core.hash_table import HashTable
from src.exceptions import (
    DuplicateKeyError,
    HashTableError,
    InvalidKeyError,
    RecordNotFoundError,
    TableOverflowError,
)
from src.models.hash_record import HashRecord
from src.presenters.table_formatter import TableFormatter


class Menu:
    def __init__(self, table: HashTable) -> None:
        self._table = table

    def run(self) -> None:
        while True:
            self._print_menu()
            choice = input("Выберите действие: ").strip()

            if choice == "1":
                self._show_table()
            elif choice == "2":
                self._search_record()
            elif choice == "3":
                self._add_record()
            elif choice == "4":
                self._delete_record()
            elif choice == "5":
                self._show_summary()
            elif choice == "0":
                print("Завершение программы.")
                return
            else:
                print("Некорректный пункт меню.")

    def _print_menu(self) -> None:
        print()
        print("1. Показать хеш-таблицу")
        print("2. Найти запись по ключу")
        print("3. Добавить запись")
        print("4. Удалить запись")
        print("5. Показать сводку")
        print("0. Выход")
        print()

    def _show_table(self) -> None:
        print(TableFormatter.format_full_report(self._table))

    def _show_summary(self) -> None:
        print(TableFormatter.format_summary(self._table))

    def _search_record(self) -> None:
        key = input("Введите ключ: ").strip()

        try:
            record = self._table.search(key)
            value = self._table.compute_value(key)
            hash_index = self._table.compute_hash(key)
            index = self._table.find_index(key)

            print("Запись найдена.")
            print(f"Ключ: {record.key}")
            print(f"Данные: {record.value}")
            print(f"V: {value}")
            print(f"h: {hash_index}")
            print(f"Индекс строки: {index}")
        except (InvalidKeyError, RecordNotFoundError) as error:
            print(error)

    def _add_record(self) -> None:
        key = input("Введите ключ: ").strip()
        value = input("Введите данные: ").strip()

        try:
            index = self._table.insert(HashRecord(key=key, value=value))
            print(f"Запись добавлена в строку {index}.")
        except (
            InvalidKeyError,
            DuplicateKeyError,
            TableOverflowError,
            HashTableError,
        ) as error:
            print(error)

    def _delete_record(self) -> None:
        key = input("Введите ключ для удаления: ").strip()

        try:
            self._table.delete(key)
            print("Запись удалена.")
        except (InvalidKeyError, RecordNotFoundError) as error:
            print(error)