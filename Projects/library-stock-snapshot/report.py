"""Report library copy availability at the end of a day."""
import argparse
from datetime import date
from pathlib import Path
import sqlite3

ROOT = Path(__file__).resolve().parent
DEMO_DAY = date(2026, 11, 24)


def availability(connection, day):
    query = (ROOT / "availability.sql").read_text(encoding="utf-8")
    return connection.execute(query, {"day": day.isoformat()}).fetchall()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("day", nargs="?", type=date.fromisoformat, default=DEMO_DAY,
                        help="snapshot date, e.g. 2026-11-24")
    day = parser.parse_args().day
    with sqlite3.connect(":memory:") as connection:
        connection.execute("PRAGMA foreign_keys = ON")
        connection.executescript((ROOT / "sample.sql").read_text(encoding="utf-8"))
        rows = availability(connection, day)
    print(f"Library stock on {day}")
    print("Title | Total | On loan | Available")
    for row in rows:
        print(" | ".join(map(str, row)))


if __name__ == "__main__":
    main()
