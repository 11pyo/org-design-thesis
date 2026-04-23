"""
Download 10-K filings for an S&P 500 sample via SEC EDGAR.

SEC requires User-Agent: NAME EMAIL and rate limit <=10 req/s. We're
far below that.

Writes each 10-K index JSON + primary .htm document to
real_data/filings/CIK/ACCESSION/
"""

from __future__ import annotations
import os, time, json, sys
import urllib.request, urllib.error
import pandas as pd
from pathlib import Path

HERE = Path(__file__).parent
UA = "Han Wonpyo unc50018441@gmail.com"
FILINGS = HERE / "filings"
FILINGS.mkdir(exist_ok=True)

SP500 = pd.read_csv(HERE / "sp500_list.csv")


def req(url: str, binary: bool = False, retries: int = 3):
    for attempt in range(retries):
        try:
            r = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(r, timeout=30) as resp:
                data = resp.read()
                return data if binary else data.decode("utf-8", errors="replace")
        except urllib.error.HTTPError as e:
            if e.code in (429, 503):
                time.sleep(2 ** attempt)
            else:
                raise
        except Exception:
            time.sleep(1)
    raise RuntimeError(f"failed to fetch {url}")


def fetch_submissions(cik: str) -> dict:
    cik_padded = str(cik).zfill(10)
    url = f"https://data.sec.gov/submissions/CIK{cik_padded}.json"
    return json.loads(req(url))


def find_10k_filings(subs: dict, since_year: int = 2018) -> list[dict]:
    recent = subs.get("filings", {}).get("recent", {})
    forms = recent.get("form", [])
    dates = recent.get("filingDate", [])
    accs = recent.get("accessionNumber", [])
    primary_docs = recent.get("primaryDocument", [])
    results = []
    for form, date, acc, doc in zip(forms, dates, accs, primary_docs):
        if form == "10-K" and date[:4] >= str(since_year):
            results.append({"form": form, "date": date, "accession": acc, "primary_doc": doc})
    return results


def download_one(cik: str, filing: dict) -> Path | None:
    cik_padded = str(cik).zfill(10)
    acc_nodash = filing["accession"].replace("-", "")
    base = f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{acc_nodash}"
    url = f"{base}/{filing['primary_doc']}"
    out_dir = FILINGS / cik_padded / acc_nodash
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / filing["primary_doc"]
    if out_file.exists() and out_file.stat().st_size > 10000:
        return out_file
    try:
        content = req(url)
        out_file.write_text(content, encoding="utf-8", errors="replace")
        meta = {**filing, "cik": cik_padded, "url": url,
                "bytes": len(content.encode("utf-8", errors="replace"))}
        (out_dir / "meta.json").write_text(json.dumps(meta, indent=2))
        return out_file
    except Exception as e:
        return None


def main(n_firms: int = 100, since_year: int = 2019):
    sample = SP500.head(n_firms)
    records = []
    for idx, row in sample.iterrows():
        cik = row["CIK"]
        sym = row["Symbol"]
        try:
            subs = fetch_submissions(cik)
        except Exception as e:
            print(f"  [{idx:3d}] {sym:6s} cik={cik}  submissions fail: {e}")
            continue
        filings_list = find_10k_filings(subs, since_year=since_year)
        got = 0
        for f in filings_list[:6]:
            path = download_one(cik, f)
            if path:
                got += 1
                records.append({
                    "cik": str(cik).zfill(10),
                    "symbol": sym,
                    "sector": row["GICS Sector"],
                    "sub_industry": row["GICS Sub-Industry"],
                    "date": f["date"],
                    "year": int(f["date"][:4]),
                    "accession": f["accession"],
                    "primary_doc": f["primary_doc"],
                    "path": str(path),
                })
            time.sleep(0.15)
        print(f"  [{idx:3d}] {sym:6s} cik={str(cik).zfill(10)}  got {got} 10-Ks")
        time.sleep(0.2)

    meta_df = pd.DataFrame(records)
    meta_df.to_csv(HERE / "filings_index.csv", index=False)
    print(f"\nTotal filings downloaded: {len(meta_df)}")
    print(meta_df.groupby("year").size())
    return meta_df


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 100
    since = int(sys.argv[2]) if len(sys.argv) > 2 else 2019
    main(n_firms=n, since_year=since)
