from src.core.hash_table import HashTable


class TableFormatter:
    @staticmethod
    def format_table(table: HashTable) -> str:
        lines = []
        header = (
            f"{'№':<3} {'ID':<18} {'C':<1} {'U':<1} {'T':<1} {'L':<1} {'D':<1} "
            f"{'P0':<3} {'Pi':<70} {'V':<4} {'h':<3}"
        )
        lines.append(header)
        lines.append("-" * len(header))

        for row in table.to_rows():
            key = row["key"] if row["key"] else "-"
            value = row["value"] if row["value"] else "-"
            next_index = row["next_index"] if row["next_index"] != -1 else "-"
            v_value = row["v"] if row["v"] is not None else "-"
            h_value = row["h"] if row["h"] is not None else "-"

            lines.append(
                f"{row['index']:<3} "
                f"{str(key):<18} "
                f"{int(bool(row['collision'])):<1} "
                f"{int(bool(row['occupied'])):<1} "
                f"{int(bool(row['terminal'])):<1} "
                f"{int(bool(row['linked'])):<1} "
                f"{int(bool(row['deleted'])):<1} "
                f"{str(next_index):<3} "
                f"{str(value):<70.70} "
                f"{str(v_value):<4} "
                f"{str(h_value):<3}"
            )

        return "\n".join(lines)

    @staticmethod
    def format_summary(table: HashTable) -> str:
        return (
            f"Размер таблицы: {table.size}\n"
            f"Количество активных записей: {table.active_count()}\n"
            f"Количество коллизий: {table.collision_count()}\n"
            f"Количество цепочек: {table.chain_count()}\n"
            f"Коэффициент заполнения: {table.load_factor():.2f}"
        )

    @staticmethod
    def format_full_report(table: HashTable) -> str:
        return f"{TableFormatter.format_summary(table)}\n\n{TableFormatter.format_table(table)}"