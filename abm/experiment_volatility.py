"""
Environmental-volatility gradient experiment.

Varies SHOCK_EVERY from 100 (essentially static) down to 3 (very volatile),
holding all else equal. Predicts Hybrid's advantage over the best pure
structure (max of V, H) scales monotonically with volatility.

This is the headline-finding test: if Hybrid dominates only in the dynamic
regime, then a volatility gradient should reveal a clean dose-response
relationship.

Writes ../results/results_volatility.csv
"""
from __future__ import annotations
import os, sys
import numpy as np
import pandas as pd
from tqdm import tqdm

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import experiment_dynamic as ed
import experiment_v2 as v2
from nk_landscape import NKLandscape


def run_one(structure, tau, K, seed, shock_every, reshuffle_frac=0.25,
            N=15, n_agents=30, T=40):
    ed.SHOCK_EVERY = shock_every
    ed.RESHUFFLE_FRAC = reshuffle_frac
    rng = np.random.default_rng(seed * 19_031 + K * 43 + int(tau * 100) + shock_every)
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
            subord = [v2.agent_best_flip(state, landscape, tau, rng)
                      for _ in range(n_agents - 1)]
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
                bit = int(rng.integers(0, N))
                states[i] ^= (1 << bit)
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
                bit = int(rng.integers(0, N))
                leader_states[c] ^= (1 << bit)
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

    return {
        "structure": structure, "tau": tau, "K": K, "seed": seed,
        "shock_every": shock_every, "reshuffle_frac": reshuffle_frac,
        "initial_fitness": fit0, "final_fitness": final_fit,
        "improvement": final_fit - fit0,
        "N": N, "n_agents": n_agents, "T": T,
    }


def main():
    shock_levels = [100, 40, 20, 10, 5, 3]
    taus = [0.2, 0.5, 0.8]
    Ks = [2, 5, 10]
    seeds = range(1, 31)

    cells = [(s, tau, K, seed, shock)
             for s in ("V", "H", "Hy")
             for shock in shock_levels
             for tau in taus
             for K in Ks
             for seed in seeds]
    print(f"volatility total runs: {len(cells)}", flush=True)
    rows = [run_one(*c) for c in tqdm(cells)]
    df = pd.DataFrame(rows)
    out = os.path.normpath(os.path.join(HERE, "..", "results", "results_volatility.csv"))
    df.to_csv(out, index=False)
    print(f"Wrote {out}", flush=True)

    g = (df.groupby(["shock_every", "K", "tau", "structure"])["final_fitness"]
         .mean().unstack("structure").reset_index())
    g["Hy_minus_best_pure"] = g["Hy"] - g[["V", "H"]].max(axis=1)
    print("\nHybrid advantage over best pure structure, by shock frequency:", flush=True)
    print(g.groupby("shock_every")["Hy_minus_best_pure"].agg(["mean", "std"]).round(4), flush=True)


if __name__ == "__main__":
    main()
