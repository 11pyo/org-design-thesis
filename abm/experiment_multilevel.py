"""
Multi-level vertical structure (resolves Critique 3).

The baseline V delegates nothing: CEO picks every firm move from subordinate
proposals. That's closer to "dictatorship" than to Burns & Stalker's
mechanistic structure.

This extension models a more realistic multi-level V:

  CEO                      tau_ceo  = min(1.0, tau * 1.3)
  5 mid-managers           tau_mgr  = min(1.0, tau * 1.15)  -- own "divisions"
  24 workers               tau_wkr  = tau

Delegation: each manager runs her own local search in her division, picks
the best move FROM HER DIVISION'S STATE every step. Divisions have
independent trajectories (like small sub-firms). Every CEO_COORD_EVERY
steps, the CEO picks the best-performing division's state and broadcasts
it firmwide -- this is the "corporate refocus" event.

This is structurally closer to Rajan-Wulf (2006) "flattening firm" data,
Csaszar (2013) "efficient frontier", and the classic Burns-Stalker
mechanistic organization.

Writes results/results_multilevel.csv.
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


def run_multilevel_V(landscape, tau, n_agents, T, rng, init_state,
                     n_divisions=5, ceo_coord_every=3, shock_every=10**9):
    tau_ceo = min(1.0, tau * 1.3)
    tau_mgr = min(1.0, tau * 1.15)
    tau_wkr = tau

    division_states = np.full(n_divisions, init_state, dtype=np.int64)
    n_workers_per = (n_agents - 1 - n_divisions) // n_divisions

    for t in range(T):
        if (t + 1) % shock_every == 0:
            ed.shock(landscape, rng)
        for d in range(n_divisions):
            s = int(division_states[d])
            proposals = []
            proposals.append(v2.agent_best_flip(s, landscape, tau_mgr, rng))
            for _ in range(n_workers_per):
                proposals.append(v2.agent_best_flip(s, landscape, tau_wkr, rng))
            fits = landscape.all_one_bit_flip_fitnesses(s)
            cur = landscape.current_fitness_idx(s)
            best_bit, best_fit = -1, cur
            for p in proposals:
                if p == -1: continue
                if fits[p] > best_fit:
                    best_bit, best_fit = p, fits[p]
            if best_bit != -1:
                division_states[d] ^= (1 << best_bit)

        if (t + 1) % ceo_coord_every == 0:
            ceo_search = v2.agent_best_flip(int(division_states[0]), landscape, tau_ceo, rng)
            if ceo_search != -1:
                fits_now = landscape.all_one_bit_flip_fitnesses(int(division_states[0]))
                cur_fit = landscape.current_fitness_idx(int(division_states[0]))
                if fits_now[ceo_search] > cur_fit:
                    division_states[0] ^= (1 << ceo_search)
            fitnesses = [landscape.fitness_idx(int(s)) for s in division_states]
            best_div = int(np.argmax(fitnesses))
            winning_state = int(division_states[best_div])
            division_states[:] = winning_state

    fitnesses = [landscape.fitness_idx(int(s)) for s in division_states]
    firm_fit = float(np.mean(fitnesses))
    return firm_fit


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
    elif structure == "ML":
        final_fit = run_multilevel_V(landscape, tau, n_agents, T, rng, init_state,
                                     shock_every=shock_every)
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

    return {"structure": structure, "tau": tau, "K": K, "seed": seed,
            "shock_every": shock_every,
            "initial_fitness": fit0, "final_fitness": final_fit}


def main():
    shock_levels = [100, 40, 20, 10, 5, 3]
    structures = ("V", "ML", "H")
    taus = (0.2, 0.5, 0.8)
    Ks = (2, 5, 10)
    seeds = range(1, 31)

    cells = [(s, tau, K, seed, se)
             for s in structures
             for se in shock_levels
             for tau in taus
             for K in Ks
             for seed in seeds]
    print(f"total runs: {len(cells)}", flush=True)
    rows = [run_one(*c) for c in tqdm(cells)]
    df = pd.DataFrame(rows)
    out = os.path.normpath(os.path.join(HERE, "..", "results", "results_multilevel.csv"))
    df.to_csv(out, index=False)
    print(f"Wrote {out}", flush=True)

    piv = (df.groupby(["shock_every", "structure"])["final_fitness"]
           .mean().unstack("structure").round(3))
    print("\nMean fitness by shock_every x structure:")
    print(piv)
    piv["ML_minus_H"] = piv["ML"] - piv["H"]
    piv["ML_minus_V"] = piv["ML"] - piv["V"]
    piv["V_minus_H"] = piv["V"] - piv["H"]
    print("\nGap comparisons:")
    print(piv[["V_minus_H", "ML_minus_H", "ML_minus_V"]])


if __name__ == "__main__":
    main()
