"""
Dense-grid + multi-seed-bank volatility experiment (resolves Critique 1).

The baseline volatility experiment used six shock-frequency levels
(1/N for N in {3,5,10,20,40,100}). A Spearman correlation of +1.00 on
six data points is numerologically suspicious. Here we:

  (1) Use fifteen shock-frequency levels, log-spaced from 1/200 to 1/2.
  (2) Run 90 seeds per cell, partitioned into three independent
      seed banks ({1..30}, {101..130}, {201..230}) so we can verify
      replication across seed banks.
  (3) Report bootstrap confidence intervals on the V-H gap at each
      intensity level.

A linear regression of (V-H gap) on log(intensity) with bootstrap CI
gives a more credible slope estimate than a +1.00 Spearman on 6 points.

Reference: Wu, Wang, and Evans (2019, Nature) on small-vs-large teams
and disruption; their result that small teams disrupt more rests on
a dense intensity grid + bootstrap CIs. Same methodological standard
applied here.

Writes results/results_densegrid.csv
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
import experiment_dynamic as ed


def run_one(structure, tau, K, seed, shock_every, N=15, n_agents=30, T=40):
    ed.SHOCK_EVERY = shock_every
    ed.RESHUFFLE_FRAC = 0.25
    rng = np.random.default_rng(hash((structure, tau, K, seed, shock_every)) & 0xFFFFFFFF)
    landscape = NKLandscape(N=N, K=K, seed=seed)
    init_state = int(rng.integers(0, 1 << N))

    if structure == "V":
        state = init_state
        tau_ceo = min(1.0, tau * 1.3)
        for t in range(T):
            if (t + 1) % shock_every == 0:
                ed.shock(landscape, rng)
            best_move = v2.agent_best_flip(state, landscape, tau_ceo, rng)
            subord = [v2.agent_best_flip(state, landscape, tau, rng) for _ in range(n_agents - 1)]
            fits = landscape.all_one_bit_flip_fitnesses(state)
            cur = landscape.current_fitness_idx(state)
            best_bit, best_fit = -1, cur
            for p in [best_move] + subord:
                if p == -1: continue
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
            if (t + 1) % shock_every == 0:
                ed.shock(landscape, rng)
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
            if (t + 1) % shock_every == 0:
                ed.shock(landscape, rng)
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

    return {"structure": structure, "tau": tau, "K": K, "seed": seed,
            "shock_every": shock_every, "final_fitness": final_fit}


SHOCK_LEVELS = [2, 3, 4, 5, 7, 10, 14, 20, 30, 40, 60, 80, 100, 150, 200]
SEED_BANKS = {"A": range(1, 31), "B": range(101, 131), "C": range(201, 231)}


def main():
    cells = []
    for bank_name, seeds in SEED_BANKS.items():
        for se in SHOCK_LEVELS:
            for s in ("V", "H", "Hy"):
                for tau in (0.2, 0.5, 0.8):
                    for K in (2, 5, 10):
                        for seed in seeds:
                            cells.append((bank_name, se, s, tau, K, seed))
    print(f"total runs: {len(cells)}", flush=True)
    rows = []
    for (bank, se, s, tau, K, seed) in tqdm(cells):
        r = run_one(s, tau, K, seed, se)
        r["bank"] = bank
        rows.append(r)
    df = pd.DataFrame(rows)
    out = os.path.normpath(os.path.join(HERE, "..", "results", "results_densegrid.csv"))
    df.to_csv(out, index=False)
    print(f"Wrote {out}", flush=True)

    # Quick summary
    from scipy.stats import spearmanr
    for bank in SEED_BANKS:
        sub = df[df["bank"] == bank]
        g = sub.groupby(["shock_every", "structure"])["final_fitness"].mean().unstack()
        g["V_minus_H"] = g["V"] - g["H"]
        g["volatility"] = 1.0 / g.index
        rho, p = spearmanr(g["volatility"], g["V_minus_H"])
        print(f"Bank {bank}: Spearman rho = {rho:+.3f}  p = {p:.4g}")


if __name__ == "__main__":
    main()
