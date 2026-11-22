import tempfile
import unittest
from datetime import date, timedelta
from pathlib import Path
from forecast import MODELS, evaluate, predict, read_sales

class ForecastTests(unittest.TestCase):
    def setUp(self):
        self.start = date(2025, 1, 6)
        self.sales = [(self.start + timedelta(days=i), (i % 7 + 1) * 10) for i in range(56)]

    def test_weekly_signal_beats_yesterday(self):
        result = evaluate(self.sales)
        self.assertEqual(result["winner"], "Last week")
        self.assertEqual(result["forecast"], 10)
        self.assertEqual(result["next_day"], self.start + timedelta(days=56))

    def test_test_period_cannot_change_selection(self):
        altered = self.sales[:-14] + [(d, 900) for d, _ in self.sales[-14:]]
        first, second = evaluate(self.sales), evaluate(altered)
        self.assertEqual(first["winner"], second["winner"])
        self.assertEqual(first["validation"], second["validation"])
        self.assertEqual(first["test"][0][2], second["test"][0][2])

    def test_weekday_median_resists_one_spike(self):
        history = [20] * 28
        history[-7] = 500
        self.assertEqual(predict(history)[MODELS[2]], 20)

    def read(self, rows):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "data.csv"
            path.write_text("date,meals\n" + "".join(f"{d},{v}\n" for d, v in rows))
            return read_sales(path)

    def test_sorting_and_zero_sales(self):
        expected = [(self.start, 0), *self.sales[1:]]
        self.assertEqual(self.read(reversed(expected)), expected)

    def test_rejects_bad_records(self):
        for extra in ([self.sales[0]], [(self.start + timedelta(days=57), 20)],
                      [(self.start + timedelta(days=56), -1)]):
            with self.subTest(extra=extra), self.assertRaises(ValueError):
                self.read(self.sales + extra)

if __name__ == "__main__":
    unittest.main()
