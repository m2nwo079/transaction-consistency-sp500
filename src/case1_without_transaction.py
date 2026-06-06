"""
Case 1 — WITHOUT Transaction
============================

Runs two related updates (a stock's `close` price and its `volume`)
with a failure injected on purpose between them, and NO transaction
control.

Expected outcome: the first update sticks, the second never runs,
so the price changes while the volume stays the same -> the database
is left in an INCONSISTENT state.

Run:  python case1_without_transaction.py
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


# ── Case 1: WITHOUT Transaction ──
print()
print("Case 1: WITHOUT Transaction")

try:
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
    conn.commit()

print("\nResult AFTER failure (NO transaction):")
print(pd.read_sql("""
    SELECT date, close, volume
    FROM stocks
    LIMIT 1
""", conn))

conn.close()
