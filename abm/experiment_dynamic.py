"""
Dynamic-landscape extension of ABM v2.

Motivation: static NK under-rewards horizontal structures because, once the
global optimum is found, there is nothing left to explore. Real firms face
environmental shocks that re-draw portions of the fitness landscape. In a
dynamic environment, horizontal organizations' parallel-exploration benefit
is predicted to widen.

Design: every SHOCK_EVERY steps, regenerate a RESHUFFLE_FRAC fraction of the
per-locus contribution tables. All else identical to experiment_v2.py.

Prediction: tau* shifts left (horizontal advantage appears at lower tau).
Magnitude of H-V gap at high tau grows.

Output: results/results_dynamic.csv
"""
from __future__ import annotations
import os, sys, copy
import numpy as np
import pandas as pd
from tqdm import tqdm

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from nk_landscape import NKLandscape
import experiment_v2 as v2

SHOCK_EVERY = 10
RESHUFFLE_FRAC = 0.25


def shock(landscape: NKLandscape, rng: np.random.Generator) -> None:
    """In-place reshuffle of RESHUFFLE_FRAC contribution tables."""
    N = landscape.N
    n_reshuffle = max(1, int(round(RESHUFFLE_FRAC * N)))
    loci = rng.choice(N, size=n_reshuffle, replace=False)
    for i in loci:
        landscape.contrib_tables[i] = rng.random(size=landscape.contrib_tables.shape[1])
    landscape._fitness_cache = landscape._precompute_all()


def run_single_dyn(structure, tau, K, seed, N=15, n_agents=30, T=40):
    rng = np.random.default_rng(seed * 17_021 + K * 41 + int(tau * 100))
    landscape = NKLandscape(N=N, K=K, seed=seed)
    init_state = int(rng.integers(0, 1 << N))
    fit0 = landscape.fitness_idx(init_state)

    fun = v2.STRUCT_FUNS[structure]

    if structure == "V":
        tau_ceo = min(1.0, tau * 1.3)
        state = init_state
        traj = [landscape.fitness_idx(state)]
        for t in range(T):
            if (t + 1) % SHOCK_EVERY == 0:
                shock(landscape, rng)
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
            traj.append(landscape.fitness_idx(state))
        final_fit = traj[-1]

    elif structure == "H":
        states = np.full(n_agents, init_state, dtype=np.int64)
        for i in range(n_agents):
            if i > 0 and rng.random() < 0.5:
                bit = int(rng.integers(0, N))
                states[i] ^= (1 << bit)
        traj = [v2._coordinated_fitness(states, landscape)]
        for t in range(T):
            if (t + 1) % SHOCK_EVERY == 0:
                shock(landscape, rng)
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
            traj.append(v2._coordinated_fitness(states, landscape))
        final_fit = traj[-1]

    else:
        cluster_size = 5
        n_clusters = max(1, n_agents // cluster_size)
        leader_states = np.full(n_clusters, init_state, dtype=np.int64)
        for c in range(1, n_clusters):
            if rng.random() < 0.5:
                bit = int(rng.integers(0, N))
                leader_states[c] ^= (1 << bit)
        traj = [v2._coordinated_fitness(leader_states, landscape)]
        for t in range(T):
            if (t + 1) % SHOCK_EVERY == 0:
                shock(landscape, rng)
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
            traj.append(v2._coordinated_fitness(leader_states, landscape))
        final_fit = traj[-1]

    return {
        "structure": structure, "tau": tau, "K": K, "seed": seed,
        "initial_fitness": fit0, "final_fitness": final_fit,
        "peak_fitness": max(traj), "improvement": final_fit - fit0,
        "N": N, "n_agents": n_agents, "T": T,
        "shock_every": SHOCK_EVERY, "reshuffle_frac": RESHUFFLE_FRAC,
    }


def main():
    cells = [(s, tau, K, seed)
             for s in ("V", "H", "Hy")
             for tau in [round(0.1 * i, 2) for i in range(1, 10)]
             for K in (2, 5, 10)
             for seed in range(1, 21)]
    print(f"dynamic total runs: {len(cells)}")
    rows = [run_single_dyn(*c) for c in tqdm(cells)]
    df = pd.DataFrame(rows)
    out = os.path.normpath(os.path.join(HERE, "..", "results", "results_dynamic.csv"))
    df.to_csv(out, index=False)
    print(f"Wrote {out}")
    piv = (df.groupby(["K", "tau", "structure"])["final_fitness"]
           .mean().unstack("structure").round(3))
    piv["H_minus_V"] = piv["H"] - piv["V"]
    print(piv[["V", "H", "H_minus_V"]])


if __name__ == "__main__":
    main()
