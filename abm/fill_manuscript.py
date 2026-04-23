"""
Inject computed summary statistics from the four new robustness CSVs
into the manuscript, replacing the '*[Results populated from ...]*' placeholders.

Run after all of:
  results/results_shocks.csv
  results/results_multilevel.csv
  results/results_heterogeneous.csv
  results/results_replication.csv
are available.
"""
from __future__ import annotations
import os, re, sys
from pathlib import Path
import pandas as pd
import numpy as np
from scipy.stats import spearmanr

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
MANUSCRIPT = ROOT / "paper" / "manuscript.md"
RESULTS = ROOT / "results"


def format_shocks():
    p = RESULTS / "results_shocks.csv"
    if not p.exists():
        return "*[results_shocks.csv not yet produced]*"
    df = pd.read_csv(p)
    g = (df.groupby(["shock_type", "intensity", "structure"])["final_fitness"]
         .mean().unstack("structure").reset_index())
    g["V_minus_H"] = g["V"] - g["H"]
    lines = ["| Shock model | Min intensity V−H | Max intensity V−H | Spearman ρ | Perm p |",
             "|---|---|---|---|---|"]
    for st, sub in g.groupby("shock_type"):
        sub = sub.sort_values("intensity")
        rho, _ = spearmanr(sub["intensity"], sub["V_minus_H"])
        x = sub["intensity"].values
        y = sub["V_minus_H"].values
        n_perm = 10_000
        rng = np.random.default_rng(2028)
        perm_rhos = [spearmanr(x, rng.permutation(y)).correlation for _ in range(n_perm)]
        p_one = float((np.array(perm_rhos) >= rho).mean()) if rho > 0 else float((np.array(perm_rhos) <= rho).mean())
        low_int_val = sub.iloc[0]["V_minus_H"]
        high_int_val = sub.iloc[-1]["V_minus_H"]
        lines.append(f"| {st} | {low_int_val:+.3f} | {high_int_val:+.3f} | {rho:+.3f} | {p_one:.4g} |")
    return "\n".join(lines)


def format_multilevel():
    p = RESULTS / "results_multilevel.csv"
    if not p.exists():
        return "*[results_multilevel.csv not yet produced]*"
    df = pd.read_csv(p)
    g = (df.groupby(["shock_every", "structure"])["final_fitness"]
         .mean().unstack("structure").reset_index())
    g = g.sort_values("shock_every", ascending=False)
    lines = ["| shock_every | V | ML-V | H | ML−H | V−H |",
             "|---|---|---|---|---|---|"]
    for _, r in g.iterrows():
        v = r.get("V", float('nan'))
        ml = r.get("ML", float('nan'))
        h = r.get("H", float('nan'))
        lines.append(f"| {int(r['shock_every'])} | {v:.3f} | {ml:.3f} | {h:.3f} | "
                     f"{ml-h:+.3f} | {v-h:+.3f} |")
    return "\n".join(lines)


def format_heterogeneous():
    p = RESULTS / "results_heterogeneous.csv"
    if not p.exists():
        return "*[results_heterogeneous.csv not yet produced]*"
    df = pd.read_csv(p)
    g = (df.groupby(["heterogeneity", "shock_every", "structure"])["final_fitness"]
         .mean().unstack("structure").reset_index())
    g["V_minus_H"] = g["V"] - g["H"]
    g["volatility"] = 1.0 / g["shock_every"]
    lines = ["| Heterogeneity regime | V−H at static | V−H at high vol | Spearman ρ |",
             "|---|---|---|---|"]
    for h, sub in g.groupby("heterogeneity"):
        sub = sub.sort_values("volatility")
        rho, _ = spearmanr(sub["volatility"], sub["V_minus_H"])
        static = sub.iloc[0]["V_minus_H"]
        highvol = sub.iloc[-1]["V_minus_H"]
        lines.append(f"| {h} | {static:+.3f} | {highvol:+.3f} | {rho:+.3f} |")
    return "\n".join(lines)


def format_replication():
    p = RESULTS / "results_replication.csv"
    if not p.exists():
        return "*[results_replication.csv not yet produced]*"
    df = pd.read_csv(p)
    g = (df.groupby(["bank", "shock_every", "structure"])["final_fitness"]
         .mean().unstack("structure").reset_index())
    g["V_minus_H"] = g["V"] - g["H"]
    g["volatility"] = 1.0 / g["shock_every"]
    lines = ["| Seed bank | V−H at shock/100 | V−H at shock/3 | Slope on log(ω) | Spearman ρ |",
             "|---|---|---|---|---|"]
    for bank, sub in g.groupby("bank"):
        sub = sub.sort_values("volatility")
        rho, _ = spearmanr(sub["volatility"], sub["V_minus_H"])
        slope, _ = np.polyfit(np.log(sub["volatility"]), sub["V_minus_H"], 1)
        low = sub[sub["shock_every"] == 100]["V_minus_H"].iloc[0] if any(sub["shock_every"] == 100) else float('nan')
        high = sub[sub["shock_every"] == 3]["V_minus_H"].iloc[0] if any(sub["shock_every"] == 3) else float('nan')
        lines.append(f"| {bank} | {low:+.3f} | {high:+.3f} | {slope:+.4f} | {rho:+.3f} |")
    return "\n".join(lines)


def main():
    md = MANUSCRIPT.read_text(encoding="utf-8")

    repl_block = format_replication()
    md = re.sub(
        r"\*\[Results populated from `results/bootstrap_summary\.json`.*?\]\*",
        "\n" + repl_block + "\n",
        md, count=1, flags=re.DOTALL,
    )

    shocks_block = format_shocks()
    md = re.sub(
        r"\*\[Table populated from `results/results_shocks\.csv`.*?\]\*",
        "\n" + shocks_block + "\n",
        md, count=1, flags=re.DOTALL,
    )

    ml_block = format_multilevel()
    md = re.sub(
        r"\*\[Results populated from `results/results_multilevel\.csv`.*?\]\*",
        "\n" + ml_block + "\n",
        md, count=1, flags=re.DOTALL,
    )

    het_block = format_heterogeneous()
    md = re.sub(
        r"\*\[Results populated from `results/results_heterogeneous\.csv`.*?\]\*",
        "\n" + het_block + "\n",
        md, count=1, flags=re.DOTALL,
    )

    MANUSCRIPT.write_text(md, encoding="utf-8")
    print("Manuscript updated with available results.")

    print("\n--- replication ---")
    print(repl_block)
    print("\n--- shocks ---")
    print(shocks_block)
    print("\n--- multilevel ---")
    print(ml_block)
    print("\n--- heterogeneous ---")
    print(het_block)


if __name__ == "__main__":
    main()
