"""
Robustness checks for the v2 ABM.

Runs three sensitivity analyses against the baseline in experiment_v2.py:

  1. FRAGMENTATION_COST sweep : {0.10, 0.20, 0.30}
       Tests sensitivity of tau* to the single dominant parameter.
  2. n_agents sweep           : {15, 30, 60}
       Tests whether horizontal advantage scales with team size.
  3. Finer tau grid           : 0.05 step around the observed crossover
       Tightens tau* estimates.

Output: results/results_robustness.csv + figures
"""
from __future__ import annotations
import os, sys
import numpy as np
import pandas as pd
from tqdm import tqdm

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from nk_landscape import NKLandscape
import experiment_v2 as v2

ROOT = os.path.normpath(os.path.join(HERE, ".."))
OUT = os.path.join(ROOT, "results", "results_robustness.csv")


def run_with_frag(frag_cost: float, cells: list[tuple]) -> list[dict]:
    original = v2.FRAGMENTATION_COST
    v2.FRAGMENTATION_COST = frag_cost
    rows = []
    try:
        for c in cells:
            r = v2.run_single_v2(*c)
            r["fragmentation_cost"] = frag_cost
            rows.append(r)
    finally:
        v2.FRAGMENTATION_COST = original
    return rows


def sweep_fragmentation():
    print("\n[sensitivity] FRAGMENTATION_COST sweep")
    cells = [(s, tau, K, seed)
             for s in ("V", "H", "Hy")
             for tau in [0.1, 0.2, 0.3, 0.4, 0.5, 0.7, 0.9]
             for K in (2, 5, 10)
             for seed in range(1, 21)]
    all_rows = []
    for fc in tqdm([0.10, 0.20, 0.30], desc="frag cost"):
        all_rows.extend(run_with_frag(fc, cells))
    return pd.DataFrame(all_rows)


def sweep_n_agents():
    print("\n[sensitivity] n_agents sweep")
    rows = []
    for n in tqdm([15, 30, 60], desc="n_agents"):
        cells = [(s, tau, K, seed)
                 for s in ("V", "H", "Hy")
                 for tau in [0.1, 0.3, 0.5, 0.7, 0.9]
                 for K in (5,)
                 for seed in range(1, 21)]
        for c in cells:
            r = v2.run_single_v2(*c, n_agents=n)
            r["n_agents_setting"] = n
            rows.append(r)
    return pd.DataFrame(rows)


def fine_tau_grid():
    print("\n[sensitivity] fine tau grid around crossover")
    cells = [(s, tau, K, seed)
             for s in ("V", "H", "Hy")
             for tau in [round(0.05 + 0.025 * i, 3) for i in range(0, 13)]
             for K in (2, 5, 10)
             for seed in range(1, 21)]
    rows = [v2.run_single_v2(*c) for c in tqdm(cells, desc="fine tau")]
    return pd.DataFrame(rows)


def main():
    dfs = {}

    df_frag = sweep_fragmentation()
    df_frag["sweep"] = "fragmentation_cost"
    dfs["frag"] = df_frag
    print("  H-V gap by frag cost x tau (K=5):")
    piv = (df_frag[df_frag["K"] == 5]
           .groupby(["fragmentation_cost", "tau", "structure"])["final_fitness"]
           .mean().unstack("structure").round(3))
    piv["H_minus_V"] = piv["H"] - piv["V"]
    print(piv[["V", "H", "H_minus_V"]])

    df_n = sweep_n_agents()
    df_n["sweep"] = "n_agents"
    dfs["n_agents"] = df_n
    print("\n  H-V gap by n_agents x tau (K=5):")
    piv2 = (df_n.groupby(["n_agents_setting", "tau", "structure"])["final_fitness"]
            .mean().unstack("structure").round(3))
    piv2["H_minus_V"] = piv2["H"] - piv2["V"]
    print(piv2[["V", "H", "H_minus_V"]])

    df_tau = fine_tau_grid()
    df_tau["sweep"] = "fine_tau"
    dfs["fine_tau"] = df_tau

    combined = pd.concat(dfs.values(), ignore_index=True)
    combined.to_csv(OUT, index=False)
    print(f"\nWrote {OUT}: {len(combined)} rows")

    print("\n  fine-grid tau* estimates:")
    g = (df_tau.groupby(["K", "tau", "structure"])["final_fitness"]
         .mean().unstack("structure").reset_index())
    g["dHV"] = g["H"] - g["V"]
    for K in sorted(g["K"].unique()):
        sub = g[g["K"] == K].sort_values("tau").reset_index(drop=True)
        xs, ys = sub["tau"].values, sub["dHV"].values
        tau_star = None
        for i in range(len(xs) - 1):
            if ys[i] * ys[i + 1] < 0:
                tau_star = xs[i] - ys[i] * (xs[i + 1] - xs[i]) / (ys[i + 1] - ys[i])
                break
        print(f"    K={K}: tau* = {tau_star}")


if __name__ == "__main__":
    main()
