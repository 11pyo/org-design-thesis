"""
Robustness to shock-model specification.

Tests whether the H5 volatility-reversal finding generalizes across
three alternative shock operationalizations:

  (1) 'periodic'   : baseline -- every N steps, 25% locus reshuffle
  (2) 'poisson'    : random timing, P(shock|step) = lambda
  (3) 'drift'      : small continuous perturbation every step
  (4) 'correlated' : shocks affect loci in correlated blocks (e.g. 3 adjacent loci)

Each produces a different 'volatility' construct. The headline claim
(volatility reverses horizontal advantage) survives if the V-H gap
is positive and monotone in volatility across all shock types.

Inspired by Siggelkow & Rivkin (2005) 'Speed and search in interdependent
organizational adaptation' and Csaszar (2013) 'An efficient frontier in
organization design'.

Writes results/results_shocks.csv
"""
from __future__ import annotations
import os, sys
import numpy as np
import pandas as pd
from tqdm import tqdm

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import experiment_v2 as v2
from nk_landscape import NKLandscape


def periodic_shock(landscape, rng, fraction=0.25):
    N = landscape.N
    n = max(1, int(round(fraction * N)))
    loci = rng.choice(N, size=n, replace=False)
    for i in loci:
        landscape.contrib_tables[i] = rng.random(size=landscape.contrib_tables.shape[1])
    landscape._fitness_cache = landscape._precompute_all()


def apply_drift(landscape, rng, magnitude=0.02):
    delta = rng.normal(0, magnitude, size=landscape.contrib_tables.shape)
    landscape.contrib_tables = np.clip(landscape.contrib_tables + delta, 0, 1)
    landscape._fitness_cache = landscape._precompute_all()


def apply_correlated_shock(landscape, rng, block_size=3, n_blocks=1):
    N = landscape.N
    for _ in range(n_blocks):
        start = int(rng.integers(0, N - block_size + 1))
        loci = list(range(start, start + block_size))
        base = rng.random(size=landscape.contrib_tables.shape[1])
        for i in loci:
            mix = 0.5
            landscape.contrib_tables[i] = (
                mix * base + (1 - mix) * rng.random(size=landscape.contrib_tables.shape[1])
            )
    landscape._fitness_cache = landscape._precompute_all()


def do_shock(shock_type, landscape, rng, intensity):
    if shock_type == "periodic":
        every_n = max(1, int(round(1 / intensity))) if intensity > 0 else 10**9
        return every_n
    elif shock_type == "poisson":
        if rng.random() < intensity:
            periodic_shock(landscape, rng, fraction=0.25)
        return None
    elif shock_type == "drift":
        apply_drift(landscape, rng, magnitude=intensity)
        return None
    elif shock_type == "correlated":
        if rng.random() < intensity:
            apply_correlated_shock(landscape, rng, block_size=3, n_blocks=1)
        return None
    else:
        raise ValueError(shock_type)


def run_single(shock_type, intensity, structure, tau, K, seed,
               N=15, n_agents=30, T=40):
    rng = np.random.default_rng(hash((shock_type, intensity, structure, tau, K, seed)) & 0xFFFFFFFF)
    landscape = NKLandscape(N=N, K=K, seed=seed)
    init_state = int(rng.integers(0, 1 << N))
    fit0 = landscape.fitness_idx(init_state)

    if shock_type == "periodic":
        every_n = do_shock(shock_type, landscape, rng, intensity)
        def should_shock(t):
            return (t + 1) % every_n == 0
        def shock_fn():
            periodic_shock(landscape, rng, fraction=0.25)
    else:
        def should_shock(t):
            return True
        def shock_fn():
            do_shock(shock_type, landscape, rng, intensity)

    if structure == "V":
        state = init_state
        tau_ceo = min(1.0, tau * 1.3)
        for t in range(T):
            if should_shock(t):
                shock_fn()
            best_move = v2.agent_best_flip(state, landscape, tau_ceo, rng)
            subord = [v2.agent_best_flip(state, landscape, tau, rng) for _ in range(n_agents - 1)]
            fits = landscape.all_one_bit_flip_fitnesses(state)
            cur = landscape.current_fitness_idx(state)
            best_bit, best_fit = -1, cur
            for p in [best_move] + subord:
                if p == -1:
                    continue
                if fits[p] > best_fit:
                    best_bit, best_fit = p, fits[p]
            if best_bit != -1:
                state ^= (1 << best_bit)
        final_fit = landscape.fitness_idx(state)
    elif structure == "H":
        states = np.full(n_agents, init_state, dtype=np.int64)
        for i in range(n_agents):
            if i > 0 and rng.random() < 0.5:
                states[i] ^= (1 << int(rng.integers(0, N)))
        for t in range(T):
            if should_shock(t):
                shock_fn()
            for i in range(n_agents):
                flip = v2.agent_best_flip(int(states[i]), landscape, tau, rng)
                if flip != -1:
                    states[i] ^= (1 << flip)
            for i in range(n_agents):
                if rng.random() < tau:
                    partner = int(rng.integers(0, n_agents))
                    if partner != i:
                        f_i = landscape.fitness_idx(int(states[i]))
                        f_p = landscape.fitness_idx(int(states[partner]))
                        if f_p > f_i:
                            states[i] = states[partner]
        final_fit = v2._coordinated_fitness(states, landscape)
    else:
        cluster_size = 5
        n_clusters = max(1, n_agents // cluster_size)
        leader_states = np.full(n_clusters, init_state, dtype=np.int64)
        for c in range(1, n_clusters):
            if rng.random() < 0.5:
                leader_states[c] ^= (1 << int(rng.integers(0, N)))
        for t in range(T):
            if should_shock(t):
                shock_fn()
            for c in range(n_clusters):
                s = int(leader_states[c])
                for _ in range(cluster_size):
                    flip = v2.agent_best_flip(s, landscape, tau, rng)
                    if flip != -1:
                        cand = s ^ (1 << flip)
                        if landscape.fitness_idx(cand) > landscape.fitness_idx(s):
                            s = cand
                leader_states[c] = s
            if rng.random() < tau:
                ranked = sorted(range(n_clusters),
                                key=lambda i: landscape.fitness_idx(int(leader_states[i])),
                                reverse=True)
                leader_states[ranked[-1]] = leader_states[ranked[0]]
        final_fit = v2._coordinated_fitness(leader_states, landscape)

    return {
        "shock_type": shock_type, "intensity": intensity,
        "structure": structure, "tau": tau, "K": K, "seed": seed,
        "initial_fitness": fit0, "final_fitness": final_fit,
        "improvement": final_fit - fit0,
    }


INTENSITY_GRID = {
    "periodic":  [0.01, 0.025, 0.05, 0.10, 0.20, 0.333],
    "poisson":   [0.01, 0.025, 0.05, 0.10, 0.20, 0.333],
    "drift":     [0.001, 0.005, 0.01, 0.02, 0.04, 0.08],
    "correlated":[0.01, 0.025, 0.05, 0.10, 0.20, 0.333],
}


def main():
    cells = [
        (st, it, s, tau, K, seed)
        for st in INTENSITY_GRID
        for it in INTENSITY_GRID[st]
        for s in ("V", "H", "Hy")
        for tau in (0.2, 0.5, 0.8)
        for K in (2, 5, 10)
        for seed in range(1, 11)
    ]
    print(f"total runs: {len(cells)}", flush=True)
    rows = [run_single(*c) for c in tqdm(cells)]
    df = pd.DataFrame(rows)
    out = os.path.normpath(os.path.join(HERE, "..", "results", "results_shocks.csv"))
    df.to_csv(out, index=False)
    print(f"Wrote {out} ({len(df)} rows)", flush=True)

    g = (df.groupby(["shock_type", "intensity", "structure"])["final_fitness"]
         .mean().unstack("structure").reset_index())
    g["V_minus_H"] = g["V"] - g["H"]
    print("\nV - H gap by (shock_type, intensity):")
    piv = g.pivot(index="intensity", columns="shock_type", values="V_minus_H").round(3)
    print(piv)

    print("\nSpearman rho(intensity, V - H) per shock type:")
    from scipy.stats import spearmanr
    for st in INTENSITY_GRID:
        sub = g[g["shock_type"] == st].sort_values("intensity")
        rho, p = spearmanr(sub["intensity"], sub["V_minus_H"])
        print(f"  {st:12s}: rho = {rho:+.3f}  p = {p:.4g}")


if __name__ == "__main__":
    main()
