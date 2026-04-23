"""
Full factorial experiment driver.

Structure in {V, H, Hy}
tau      in {0.1, 0.2, ..., 0.9}
K        in {2, 5, 10}
seed     1..SEEDS

Writes ../results/results.csv

Run: python experiment.py
"""

from __future__ import annotations
import os
import sys
import time
import numpy as np
import pandas as pd
from tqdm import tqdm

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nk_landscape import NKLandscape
from agents import build_agents
from organizations import STEP_FUNS


def run_single(structure: str, tau: float, K: int, seed: int,
               N: int = 15, n_agents: int = 30, T: int = 40) -> dict:
    rng = np.random.default_rng(seed * 10_007 + K * 31 + int(tau * 100))

    landscape = NKLandscape(N=N, K=K, seed=seed)
    agents = build_agents(structure, tau, n_agents)
    step_fun = STEP_FUNS[structure]

    state_int = int(rng.integers(0, 1 << N))
    fit0 = landscape.fitness_idx(state_int)
    fit_trajectory = [fit0]

    for _ in range(T):
        state_int = step_fun(agents, state_int, landscape, rng)
        fit_trajectory.append(landscape.fitness_idx(state_int))

    final_fit = fit_trajectory[-1]
    peak_fit = max(fit_trajectory)
    target = fit0 + 0.95 * (peak_fit - fit0)
    steps_to_95 = T
    for t, f in enumerate(fit_trajectory):
        if f >= target:
            steps_to_95 = t
            break

    improvements = sum(1 for i in range(1, len(fit_trajectory))
                       if fit_trajectory[i] > fit_trajectory[i - 1])
    stalls = sum(1 for i in range(1, len(fit_trajectory))
                 if fit_trajectory[i] == fit_trajectory[i - 1])

    return {
        "structure": structure,
        "tau": tau,
        "K": K,
        "seed": seed,
        "initial_fitness": fit0,
        "final_fitness": final_fit,
        "peak_fitness": peak_fit,
        "improvement": final_fit - fit0,
        "steps_to_95pct": steps_to_95,
        "n_improvements": improvements,
        "n_stalls": stalls,
        "N": N,
        "n_agents": n_agents,
        "T": T,
    }


def run_full_factorial(out_path: str,
                       structures=("V", "H", "Hy"),
                       taus=tuple(round(0.1 * i, 2) for i in range(1, 10)),
                       Ks=(2, 5, 10),
                       seeds=range(1, 41),
                       N: int = 15,
                       n_agents: int = 30,
                       T: int = 40) -> pd.DataFrame:
    cells = [
        (s, tau, K, seed)
        for s in structures
        for tau in taus
        for K in Ks
        for seed in seeds
    ]
    print(f"Total runs: {len(cells)} "
          f"(structures={len(structures)}, taus={len(taus)}, "
          f"Ks={len(Ks)}, seeds={len(list(seeds))})")

    t0 = time.time()
    rows = []
    for cell in tqdm(cells, desc="ABM runs"):
        rows.append(run_single(*cell, N=N, n_agents=n_agents, T=T))

    df = pd.DataFrame(rows)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    df.to_csv(out_path, index=False)
    elapsed = time.time() - t0
    print(f"Done in {elapsed:.1f}s. Wrote {out_path} ({len(df)} rows).")
    return df


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    out_path = os.path.normpath(os.path.join(here, "..", "results", "results.csv"))
    df = run_full_factorial(out_path)
    print("\nPreview:")
    print(df.groupby(["structure", "tau", "K"])["final_fitness"]
            .mean().unstack("structure").head(12))
