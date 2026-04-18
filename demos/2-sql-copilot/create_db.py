from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd

DB_PATH = Path("demos/02-sql-copilot/demo.db")
DATA_PATH = Path("datasets/sales.csv")


def main() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(DATA_PATH)

    con = sqlite3.connect(DB_PATH)
    df.to_sql("sales", con, if_exists="replace", index=False)

    cur = con.cursor()
    cur.execute("CREATE INDEX IF NOT EXISTS idx_sales_date ON sales(date)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_sales_category ON sales(category)")
    con.commit()
    con.close()
    print(f"DB criado em: {DB_PATH}")


if __name__ == "__main__":
    main()
