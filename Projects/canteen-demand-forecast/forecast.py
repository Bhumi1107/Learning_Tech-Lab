"""Forecast next-day meal demand and compare simple models in date order."""

import argparse
import csv
from datetime import date, timedelta
from pathlib import Path
from statistics import mean, median

ROOT = Path(__file__).resolve().parent
WINDOW = 28
PERIOD = 14
MODELS = ("Yesterday", "Last week", "Weekday median")


def read_sales(path):
    with Path(path).open(encoding="utf-8-sig", newline="") as stream:
        rows = csv.DictReader(stream)
        if not {"date", "meals"}.issubset(rows.fieldnames or []):
            raise ValueError("CSV must include date and meals columns")
        sales = {}
        for row in rows:
            try:
                day = date.fromisoformat(row["date"] or "")
                meals = int(row["meals"] or "")
            except ValueError as exc:
                raise ValueError(f"Invalid date or meal count at CSV line {rows.line_num}") from exc
            if meals < 0 or day in sales:
                raise ValueError(f"Duplicate date or negative count at CSV line {rows.line_num}")
            sales[day] = meals
    ordered = sorted(sales)
    if len(ordered) < WINDOW + 2 * PERIOD:
        raise ValueError("Include at least 56 consecutive daily totals")
    if (ordered[-1] - ordered[0]).days + 1 != len(ordered):
        raise ValueError("Supply a row for every date, using zero only for verified zero sales")
    return [(day, sales[day]) for day in ordered]


def predict(history):
    """Only the 28 observations strictly before a forecast date are available."""
    previous_weeks = [history[-lag] for lag in (7, 14, 21, 28)]
    return dict(zip(MODELS, (history[-1], history[-7], int(median(previous_weeks) + 0.5))))


def mae(rows, model):
    return mean(abs(actual - predictions[model]) for _, actual, predictions in rows)


def evaluate(sales):
    values = [count for _, count in sales]
    start = len(sales) - PERIOD * 2
    scored = [(sales[i][0], values[i], predict(values[i - WINDOW:i]))
              for i in range(start, len(sales))]
    validation, test = scored[:PERIOD], scored[PERIOD:]
    winner = min(MODELS, key=lambda model: mae(validation, model))
    return {
        "winner": winner, "validation": validation, "test": test,
        "next_day": sales[-1][0] + timedelta(days=1),
        "forecast": predict(values[-WINDOW:])[winner],
    }


def write_predictions(rows, path):
    with Path(path).open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream)
        writer.writerow(["date", "actual", *MODELS])
        for day, actual, forecasts in rows:
            writer.writerow([day, actual, *(forecasts[m] for m in MODELS)])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv", nargs="?", type=Path, default=ROOT / "data" / "sample.csv")
    parser.add_argument("--report", type=Path, help="Write a standalone HTML report")
    parser.add_argument("--predictions", type=Path, help="Write final 14 days of predictions as CSV")
    args = parser.parse_args()
    try:
        result = evaluate(read_sales(args.csv))
        if args.report:
            from report import write_report
            write_report(result, args.report)
        if args.predictions:
            write_predictions(result["test"], args.predictions)
    except (OSError, ValueError, csv.Error) as exc:
        parser.exit(2, f"Input/output error: {exc}\n")

    print(f"{'Model':<18} {'Validation MAE':>14} {'Test MAE':>12}")
    for model in MODELS:
        print(f"{model:<18} {mae(result['validation'], model):>14.2f} "
              f"{mae(result['test'], model):>12.2f}")
    print(f"Selected on validation: {result['winner']}")
    print(f"Forecast for {result['next_day']}: {result['forecast']} meals")


if __name__ == "__main__":
    main()
