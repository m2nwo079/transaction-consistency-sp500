"""
Case 2 — WITH Transaction
=========================

Runs the same two related updates (a stock's `close` price and its
`volume`) with the same failure injected on purpose between them, but
this time wrapped in a transaction (BEGIN ... ROLLBACK on error).

Expected outcome: the failure triggers a ROLLBACK, so neither update
sticks and the database stays in a CONSISTENT state.

Run:  python case2_with_transaction.py
"""

import sqlite3
import pandas as pd

# Path to the S&P 500 5-year daily dataset (all_stocks_5yr.csv).
# NOTE: the original notebook used the Google Colab path
#       "/content/all_stocks_5yr.csv". Point this at your local copy.
CSV_PATH = "data/sample.csv"


# ── Setup: load the data into a SQLite table (shared by both cases) ──
df = pd.read_csv(CSV_PATH)

print(f"Columns:{df.columns}")

conn = sqlite3.connect("stocks.db")
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS stocks")
df.to_sql("stocks", conn, index=False)

print("\nInitial Data Sample:")
print(pd.read_sql("SELECT date, close, volume FROM stocks LIMIT 5", conn))


# ── Case 2: WITH Transaction ──
print()
print("Case 2: WITH Transaction")

try:
    conn.execute("BEGIN")

    cursor.execute("""
        UPDATE stocks
        SET close = close * 1.1
        WHERE date = (SELECT date FROM stocks LIMIT 1)
    """)

    raise Exception("Simulated Failure!")

    cursor.execute("""
        UPDATE stocks
        SET volume = volume * 1.1
        WHERE date = (SELECT date FROM stocks LIMIT 1)
    """)

    conn.commit()

except Exception as e:
    print("Error occurred:", e)
    conn.rollback()

print("\nResult AFTER rollback (WITH transaction):")
print(pd.read_sql("""
    SELECT date, close, volume
    FROM stocks
    LIMIT 1
""", conn))

conn.close()
