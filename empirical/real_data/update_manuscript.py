"""
Inject real-data regression results into manuscript.md's Section 4.3 Results.

Reads regression_real_summary.csv and the implied-tau* output, then replaces
the TBD placeholders in the manuscript.

Run after regression_real.py completes.
"""
from __future__ import annotations
from pathlib import Path
import pandas as pd
import re

ROOT = Path(__file__).resolve().parents[2]
MANUSCRIPT = ROOT / "paper" / "manuscript.md"
SUMMARY = Path(__file__).parent / "regression_real_summary.csv"


def main():
    if not SUMMARY.exists():
        print(f"Missing {SUMMARY}; run regression_real.py first")
        return
    sm = pd.read_csv(SUMMARY)
    print("Regression summary:")
    print(sm.to_string(index=False))

    def fmt(row):
        est, se, pv, n = row["estimate"], row["se"], row["p"], row["n"]
        star = "***" if pv < 0.01 else "**" if pv < 0.05 else "*" if pv < 0.1 else ""
        return f"{est:+.4f}{star} ({se:.4f})", f"{pv:.4g}", f"{int(n)}"

    rows = {r["test"]: fmt(r) for _, r in sm.iterrows()}

    md = MANUSCRIPT.read_text(encoding="utf-8")

    labels = {
        "H1": "H1 (low-τ subsample) | flat",
        "H2": "H2 (high-τ subsample) | flat",
        "H3": "H3 (moderation) | flat × τ",
        "H4": "H4 (triple interaction) | flat × τ × K",
    }

    block = ["| Test | Coefficient | Estimate | SE | p | n |",
             "|---|---|---|---|---|---|"]
    for k, lab in labels.items():
        if k in rows:
            est, pv, n = rows[k]
            block.append(f"| {lab} | {est} | {pv} | {n} |")
        else:
            block.append(f"| {lab} | — | — | — |")
    new_table = "\n".join(block)

    pattern = re.compile(
        r"\| Test \| Coefficient \| Estimate \| SE \| p \| n \|.*?\| H4 \(triple interaction\).*?\n",
        re.DOTALL,
    )
    if pattern.search(md):
        md = pattern.sub(new_table + "\n", md, count=1)
    else:
        md = md.replace(
            "| H4 (triple interaction) | flat × τ × K | TBD | TBD | TBD | TBD |",
            block[-1]
        )
        for k, lab in labels.items():
            if k in rows:
                est, pv, n = rows[k]
                md = md.replace(
                    f"| {lab} | TBD | TBD | TBD | TBD |",
                    f"| {lab} | {est} | {pv} | {n} |"
                )

    MANUSCRIPT.write_text(md, encoding="utf-8")
    print(f"Updated {MANUSCRIPT}")
    print("\n" + new_table)


if __name__ == "__main__":
    main()
