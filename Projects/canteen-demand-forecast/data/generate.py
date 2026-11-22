"""Recreate the fictional 16-week canteen series using a fixed random seed."""
import csv
from datetime import date, timedelta
from pathlib import Path
from random import Random

def generate(path):
    rng = Random(1107)
    start = date(2025, 1, 6)
    weekday_sales = [122, 146, 134, 155, 114, 68, 42]
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream, lineterminator="\n")
        writer.writerow(["date", "meals"])
        for i in range(112):
            day = start + timedelta(days=i)
            base = weekday_sales[day.weekday()]
            event = 35 if i in (17, 40, 66, 94, 107) else 0
            writer.writerow([day, base + i // 28 + rng.randint(-12, 12) + event])

if __name__ == "__main__":
    generate(Path(__file__).with_name("sample.csv"))
