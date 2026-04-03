from pathlib import Path
import runpy

from src.main import build_default_table, main
from src.menu import Menu


def test_build_default_table_creates_prefilled_hash_table() -> None:
    table = build_default_table()

    assert table.size == 20
    assert table.active_count() >= 10
    assert table.collision_count() >= 2
    assert table.chain_count() >= 3


def test_main_calls_menu_run(monkeypatch) -> None:
    called = {"value": False}

    def fake_run(self) -> None:
        called["value"] = True

    monkeypatch.setattr(Menu, "run", fake_run)

    main()

    assert called["value"] is True


def test_main_file_entry_point_runs(monkeypatch) -> None:
    called = {"value": False}

    def fake_run(self) -> None:
        called["value"] = True

    monkeypatch.setattr(Menu, "run", fake_run)

    main_file = Path(__file__).resolve().parents[1] / "src" / "main.py"
    runpy.run_path(str(main_file), run_name="__main__")

    assert called["value"] is True