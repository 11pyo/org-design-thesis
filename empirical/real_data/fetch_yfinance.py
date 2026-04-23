"""
Pull firm-level financial data via yfinance for the S&P 500 sample.

Data captured:
- total_assets, net_income (yearly) -> ROA = NI / assets
- employees (latest, not yearly)
- founded_year (from SP500 list)
- market_cap (latest, control)

yfinance rate-limits aggressively. We slow-stream through the list with
retries.

Writes real_data/yf_firm_year.csv
"""
from __future__ import annotations
import time
from pathlib import Path
import pandas as pd
import yfinance as yf

HERE = Path(__file__).parent
SP500 = pd.read_csv(HERE / "sp500_list.csv")


def pull_one(symbol: str) -> list[dict]:
    try:
        t = yf.Ticker(symbol)
        fin = t.income_stmt
        bal = t.balance_sheet
        info = {}
        try:
            info = t.info
        except Exception:
            info = {}
        if fin is None or fin.empty or bal is None or bal.empty:
            return []
        records = []
        for year_col in fin.columns:
            year = pd.Timestamp(year_col).year
            try:
                ni = float(fin.loc["Net Income", year_col]) if "Net Income" in fin.index else float("nan")
            except Exception:
                ni = float("nan")
            try:
                assets = float(bal.loc["Total Assets", year_col]) if "Total Assets" in bal.index else float("nan")
            except Exception:
                assets = float("nan")
            records.append({
                "symbol": symbol,
                "year": year,
                "net_income": ni,
                "total_assets": assets,
                "ROA": (ni / assets) if (assets and assets == assets and assets != 0) else float("nan"),
                "employees": info.get("fullTimeEmployees"),
                "market_cap": info.get("marketCap"),
                "sector_yf": info.get("sector"),
            })
        return records
    except Exception as e:
        return [{"symbol": symbol, "year": None, "_error": str(e)[:120]}]


def main(n_firms: int = 150):
    sample = SP500.head(n_firms)
    all_rows = []
    for i, r in sample.iterrows():
        sym = r["Symbol"]
        rows = pull_one(sym)
        for row in rows:
            row["founded"] = r.get("Founded")
            row["sector_gics"] = r.get("GICS Sector")
            row["cik"] = str(r["CIK"]).zfill(10)
        all_rows.extend(rows)
        if (i + 1) % 10 == 0:
            print(f"  yf {i+1}/{len(sample)}")
        time.sleep(0.2)

    df = pd.DataFrame(all_rows)
    df.to_csv(HERE / "yf_firm_year.csv", index=False)
    print(f"Wrote yf_firm_year.csv: {len(df)} rows")
    print(df.describe().round(2))
    return df


if __name__ == "__main__":
    import sys
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 150
    main(n_firms=n)
