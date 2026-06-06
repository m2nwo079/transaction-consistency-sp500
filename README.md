# transaction-consistency-sp500

Database transaction **atomicity & consistency** demonstrated with Python and SQLite on real S&P 500 market data. This repository accompanies a presentation for *Database Management* (ITM, SeoulTech): the slides explain the theory, and the source code reproduces it on actual data.

## Live presentation

The slide deck is published with GitHub Pages:

**https://m2nwo079.github.io/transaction-consistency-sp500/**

Navigate with the arrow keys (← / →), spacebar, mouse clicks, or swipe on mobile.

## What it demonstrates

The same two database updates — a stock's `close` price and its `volume` — are run with a failure deliberately injected in the middle:

- **Without a transaction** (`case1_without_transaction.py`) — the first update is applied but the second never runs, leaving the price changed and the volume unchanged. The database ends up in an inconsistent state.
- **With a transaction** (`case2_with_transaction.py`) — the same failure triggers a `ROLLBACK`, so neither update sticks and the database stays consistent.

Concepts covered: the ACID properties, the Partial Write Problem, the Write-Ahead Log (WAL), and application-level versus DBMS-level transaction control.

## Repository structure

```
transaction-consistency-sp500/
├── index.html                         # presentation slides (served by GitHub Pages)
├── src/
│   ├── case1_without_transaction.py   # no transaction -> inconsistent state
│   └── case2_with_transaction.py      # with transaction -> rollback keeps it consistent
├── data/
│   └── sample.csv                     # small bundled sample so the scripts run immediately
├── requirements.txt
├── .gitignore
├── .gitattributes
├── LICENSE
└── README.md
```

## Data

The scripts read a price CSV with the columns `date, open, high, low, close, volume, Name`.

- A tiny **illustrative sample** (`data/sample.csv`, synthetic values) is bundled so the scripts run out of the box with no download required.
- For the exact figures shown in the slides, use the full dataset — the **"S&P 500 stock data"** dataset on Kaggle (`all_stocks_5yr.csv`):
  https://www.kaggle.com/datasets/camnugent/sandp500
  Download it into `data/`, then set `CSV_PATH` at the top of each script to `data/all_stocks_5yr.csv`. The full dataset is large and is not tracked in this repository (see `.gitignore`).

## Running the demo

SQLite ships with Python through the built-in `sqlite3` module, so only pandas needs to be installed:

```bash
pip install -r requirements.txt

python src/case1_without_transaction.py   # Case 1 — without transaction
python src/case2_with_transaction.py      # Case 2 — with transaction
```

Each script is self-contained: it loads the CSV into a fresh SQLite table and then runs its case.

## Tech stack

- Python (pandas)
- SQLite (`sqlite3` standard library)

## References

- ScienceDirect — Atomic transaction: https://www.sciencedirect.com/topics/computer-science/atomic-transaction
- Architecture Weekly — The Write-Ahead Log: a foundation: https://www.architecture-weekly.com/p/the-write-ahead-log-a-foundation
- CMU 15-445 Database Systems course notes: https://hrus.in/ocw/CMU15445/
- SQLite documentation: https://sqlite.org/docs.html
- SQLite — Transactions: https://www.sqlite.org/lang_transaction.html

## License

Released under the MIT License — see [LICENSE](LICENSE).

## Author

Lee Min-Woo — Database Management, ITM, SeoulTech

