"""
Multi-seed-bank replication for Critique 1 (statistical robustness).

Replicates the six-level volatility baseline using three independent
seed banks. If the V-H dose-response holds across all three banks,
the +1.00 Spearman on the baseline is not an artifact of the specific
seeds drawn.

Shock levels: same 6 as the baseline experiment_volatility.py.
Seeds per bank: 20.
Parameters: 3 structures, 3 taus, 3 Ks (identical to baseline).
Banks: {1..20}, {101..120}, {201..220}.

Total runs: 3 × 6 × 3 × 3 × 3 × 20 = 9,720. ~25 min solo, longer under contention.

Writes results/results_replication.csv
"""
from __future__ import annotations
import os, sys
import numpy as np
import pandas as pd
from tqdm import tqdm

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import experiment_v2 as v2
import experiment_dynamic as ed
from nk_landscape import NKLandscape


def run_one(structure, tau, K, seed, shock_every, N=15, n_agents=30, T=40):
    rng = np.random.default_rng(hash((structure, tau, K, seed, shock_every)) & 0xFFFFFFFF)
    landscape = NKLandscape(N=N, K=K, seed=seed)
    init_state = int(rng.integers(0, 1 << N))
    fit0 = landscape.fitness_idx(init_state)

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
            "shock_every": shock_every,
            "initial_fitness": fit0, "final_fitness": final_fit}


SHOCK_LEVELS = [100, 40, 20, 10, 5, 3]
SEED_BANKS = {"A": range(1, 11), "B": range(101, 111), "C": range(201, 211)}


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
    out = os.path.normpath(os.path.join(HERE, "..", "results", "results_replication.csv"))
    df.to_csv(out, index=False)
    print(f"Wrote {out}", flush=True)

    from scipy.stats import spearmanr
    print("\nSpearman rho(volatility, V - H) per seed bank:")
    for bank in SEED_BANKS:
        sub = df[df["bank"] == bank]
        g = sub.groupby(["shock_every", "structure"])["final_fitness"].mean().unstack()
        g["V_minus_H"] = g["V"] - g["H"]
        g["volatility"] = 1.0 / g.index
        g = g.sort_values("volatility")
        rho, p = spearmanr(g["volatility"], g["V_minus_H"])
        print(f"  Bank {bank}: rho = {rho:+.3f}  p = {p:.4g}")
        print(f"          V-H at shock/100 = {g.loc[100, 'V_minus_H']:+.4f}")
        print(f"          V-H at shock/3   = {g.loc[3, 'V_minus_H']:+.4f}")


if __name__ == "__main__":
    main()
