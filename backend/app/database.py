import json
import sqlite3
from collections.abc import Iterator
from contextlib import closing, contextmanager
from pathlib import Path

from .schemas import CocktailDetail

APP_DIR = Path(__file__).resolve().parent
DATABASE_PATH = APP_DIR.parent / "var" / "sipwise.sqlite3"
FIXTURE_PATH = APP_DIR / "data" / "cocktails_fixture.json"


@contextmanager
def connect() -> Iterator[sqlite3.Connection]:
    with closing(sqlite3.connect(DATABASE_PATH)) as connection:
        connection.execute("PRAGMA foreign_keys = ON")
        with connection:
            yield connection


def initialize() -> None:
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with connect() as connection:
        connection.execute(
            "CREATE TABLE IF NOT EXISTS cocktails "
            "(id TEXT PRIMARY KEY NOT NULL, payload_json TEXT NOT NULL)"
        )
        # Starter data for local integration. D03 replaces this seed with the catalog service.
        data = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
        recipes = [CocktailDetail.model_validate(item) for item in data]
        connection.executemany(
            "INSERT INTO cocktails (id, payload_json) VALUES (?, ?) "
            "ON CONFLICT (id) DO UPDATE SET payload_json = excluded.payload_json",
            [(recipe.id, recipe.model_dump_json()) for recipe in recipes],
        )
