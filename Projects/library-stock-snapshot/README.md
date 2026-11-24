# Library Stock Snapshot

How many copies of a book were available at closing time on a given date? This SQLite report reconstructs stock from checkout and return dates. It includes catalog titles with zero copies.

## Run the example

From this project folder, use Python 3.9 or newer. Python creates the fictional sample database in memory each time.

```sh
python report.py 2026-11-24
python -m unittest -v
```

Expected output from the report:

```text
Library stock on 2026-11-24
Title | Total | On loan | Available
Database Systems | 2 | 1 | 1
Graph Theory | 0 | 0 | 0
Python Basics | 1 | 0 | 1
```

## Why count copies first?

One physical copy can appear in several loan records. [The query](availability.sql) uses `EXISTS` to produce one on-loan flag per copy before counting by book. A final `LEFT JOIN` keeps every catalog title in the report. The sample assumes a fixed inventory over the reporting period.

**Try the return boundary.** Run `python report.py 2026-11-23`, then run the example above. The observed number of available *Database Systems* copies changes from **0 to 1**. Copy 101 comes back on 24 November and is available at closing time. Copy 102 is still on loan. The tests also cover a returned copy being checked out again on the same day.

Edit [sample.sql](sample.sql) to try another checkout. Use ISO dates (YYYY-MM-DD) and leave the return date NULL for an open loan.
