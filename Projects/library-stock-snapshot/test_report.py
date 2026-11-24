import sqlite3
import unittest
from datetime import date

from report import ROOT, availability


class SnapshotTests(unittest.TestCase):
    def setUp(self):
        self.db = sqlite3.connect(":memory:")
        self.addCleanup(self.db.close)
        self.db.execute("PRAGMA foreign_keys = ON")
        self.db.executescript((ROOT / "sample.sql").read_text(encoding="utf-8"))

    def snapshot(self, day):
        return availability(self.db, date.fromisoformat(day))

    def test_demo(self):
        self.assertEqual(self.snapshot("2026-11-24"), [
            ("Database Systems", 2, 1, 1), ("Graph Theory", 0, 0, 0),
            ("Python Basics", 1, 0, 1)])

    def test_return_boundary_and_repeated_loans(self):
        self.assertIn(("Database Systems", 2, 2, 0), self.snapshot("2026-11-23"))
        self.assertIn(("Database Systems", 2, 1, 1), self.snapshot("2026-11-24"))

    def test_future_checkout_starts_on_its_date(self):
        self.assertIn(("Python Basics", 1, 0, 1), self.snapshot("2026-11-24"))
        self.assertIn(("Python Basics", 1, 1, 0), self.snapshot("2026-11-25"))

    def test_same_day_return_and_reloan(self):
        self.db.execute("INSERT INTO loans VALUES (5, 101, '2026-11-24', NULL)")
        self.assertIn(("Database Systems", 2, 2, 0), self.snapshot("2026-11-24"))

    def test_identical_titles_are_separate_catalog_entries(self):
        self.db.execute("INSERT INTO books VALUES (4, 'Database Systems')")
        rows = self.snapshot("2026-11-24")
        self.assertIn(("Database Systems", 0, 0, 0), rows)
        self.assertIn(("Database Systems", 2, 1, 1), rows)

    def test_empty_catalog(self):
        for table in ("loans", "copies", "books"):
            self.db.execute(f"DELETE FROM {table}")
        self.assertEqual(self.snapshot("2026-11-24"), [])
