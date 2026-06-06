"""
Transaction & Data Consistency — S&P 500 demonstration
=======================================================

Shows the difference between running two related database updates
(a stock's `close` price and its `volume`) WITHOUT and WITH a
transaction, using a failure that is injected on purpose in the
middle of the two updates.

- Case 1 (no transaction): the first update sticks, the second never
  runs -> the database is left in an inconsistent state.
- Case 2 (with transaction): the same failure triggers a ROLLBACK,
  so neither update sticks -> the database stays consistent.

Tech: Python + pandas + SQLite (sqlite3 standard library).
"""

import sqlite3
import pandas as pd

# Path to the S&P 500 5-year daily dataset (all_stocks_5yr.csv).
# NOTE: the original notebook used the Google Colab path
#       "/content/all_stocks_5yr.csv". Point this at your local copy.
CSV_PATH = "data/all_stocks_5yr.csv"


# ──────────────────────────────────────────────────────────────
# Setup: load the data into a SQLite table
# ──────────────────────────────────────────────────────────────
df = pd.read_csv(CSV_PATH)

print(f"Columns:{df.columns}")

conn = sqlite3.connect("stocks.db")
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS stocks")
df.to_sql("stocks", conn, index=False)

print("\nInitial Data Sample:")
print(pd.read_sql("SELECT date, close, volume FROM stocks LIMIT 5", conn))


# ──────────────────────────────────────────────────────────────
# Case 1: WITHOUT Transaction
# ──────────────────────────────────────────────────────────────
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

# Reset the table so Case 2 starts from the original data
cursor.execute("DROP TABLE stocks")
df.to_sql("stocks", conn, index=False)


# ──────────────────────────────────────────────────────────────
# Case 2: WITH Transaction
# ──────────────────────────────────────────────────────────────
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
