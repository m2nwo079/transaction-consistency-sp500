# transaction-consistency-sp500

Database transaction **atomicity & consistency** demonstrated with Python and SQLite on real S&P 500 market data. This repository accompanies a presentation for *Database Management* (ITM, SeoulTech): the slides explain the theory, and the source code reproduces it on actual data.

## Live presentation

The slide deck is published with GitHub Pages:

**https://m2nwo079.github.io/transaction-consistency-sp500/**

Navigate with the arrow keys (← / →), spacebar, mouse clicks, or swipe on mobile.

## What it demonstrates

The same two database updates — a stock's `close` price and its `volume` — are run twice, with a failure deliberately injected in the middle:

- **Without a transaction** — the first update is applied but the second never runs, leaving the price changed and the volume unchanged. The database ends up in an inconsistent state.
- **With a transaction** — the same failure triggers a `ROLLBACK`, so neither update sticks and the database stays consistent.

Concepts covered: the ACID properties, the Partial Write Problem, the Write-Ahead Log (WAL), and application-level versus DBMS-level transaction control.

## Repository structure

```
transaction-consistency-sp500/
├── index.html              # presentation slides (served by GitHub Pages)
├── src/
│   └── transaction_demo.py # Python + SQLite demonstration
├── data/                   # place all_stocks_5yr.csv here (not tracked)
└── README.md
```

(Adjust the layout to match your own files — for example, splitting the demo into separate scripts per case.)

## Running the demo

SQLite is included with Python through the built-in `sqlite3` module, so only pandas needs to be installed:

```bash
pip install pandas
python src/transaction_demo.py
```

Before running, download the S&P 500 5-year daily price dataset (`all_stocks_5yr.csv`) into the `data/` folder, and make sure the file path in the script points to it (the original was written for Google Colab at `/content/all_stocks_5yr.csv`).

## Tech stack

- Python (pandas)
- SQLite (`sqlite3` standard library)

## References

- ScienceDirect — Atomic transaction: https://www.sciencedirect.com/topics/computer-science/atomic-transaction
- Architecture Weekly — The Write-Ahead Log: a foundation: https://www.architecture-weekly.com/p/the-write-ahead-log-a-foundation
- CMU 15-445 Database Systems course notes: https://hrus.in/ocw/CMU15445/
- SQLite documentation: https://sqlite.org/docs.html
- SQLite — Transactions: https://www.sqlite.org/lang_transaction.html

## Author

Lee Min-Woo (23102017) — Database Management, ITM, SeoulTech
