"""
Experiment variant 2: independent-search model.

In v1 (experiment.py) all agents share one firm state and the structure
decides how to aggregate their proposals into the next firm state. This
emphasizes decision-making rules (consensus vs authority) but under-weights
the EXPLORATION diversity that horizontal organizations gain in real life.

v2 adds diversity explicitly:

- Each agent maintains their OWN current state.
- Each step they search locally (tau-gated) and greedily climb.
- Structure determines inter-agent coupling:
    * V (vertical):   at each step, all agents reset to CEO's state.
                      CEO then applies her best move. High convergence.
    * H (horizontal): agents keep their own states; they share discoveries
                      with probability tau each step (communication quality).
                      Firm fitness = max over agents (firm harvests the best).
    * Hy (hybrid):    agents reset to cluster-leader state each step within
                      cluster. Cluster leaders share across cluster with
                      prob tau. Firm fitness = max over leaders.

This captures Lazer-Friedman (2007): dense networks converge fast to local
optima; sparse networks preserve diversity, find better global optima at
the cost of slower convergence.

Writes ../results/results_v2.csv
"""

from __future__ import annotations
import os
import sys
import numpy as np
import pandas as pd
from tqdm import tqdm

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nk_landscape import NKLandscape


def agent_best_flip(state_int: int, landscape: NKLandscape,
                    tau: float, rng: np.random.Generator) -> int:
    N = landscape.N
    k_visible = max(1, int(round(tau * N)))
    visible = rng.choice(N, size=k_visible, replace=False)
    neighbor_fits = landscape.all_one_bit_flip_fitnesses(state_int)
    current = landscape.current_fitness_idx(state_int)
    best_idx, best_fit = -1, current
    for b in visible:
        if neighbor_fits[b] > best_fit:
            best_fit, best_idx = neighbor_fits[b], int(b)
    return best_idx


def run_vertical(landscape, tau, n_agents, T, rng, init_state):
    tau_ceo = min(1.0, tau * 1.3)
    state = init_state
    fit_traj = [landscape.fitness_idx(state)]
    for _ in range(T):
        best_move = agent_best_flip(state, landscape, tau_ceo, rng)
        subordinate_props = [
            agent_best_flip(state, landscape, tau, rng)
            for _ in range(n_agents - 1)
        ]
        fits = landscape.all_one_bit_flip_fitnesses(state)
        cur = landscape.current_fitness_idx(state)
        candidates = [best_move] + subordinate_props
        best_bit, best_fit = -1, cur
        for p in candidates:
            if p == -1:
                continue
            if fits[p] > best_fit:
                best_bit, best_fit = p, fits[p]
        if best_bit != -1:
            state ^= (1 << best_bit)
        fit_traj.append(landscape.fitness_idx(state))
    return state, fit_traj, landscape.fitness_idx(state)


FRAGMENTATION_COST = 0.20


def _mode_and_concentration(states: np.ndarray) -> tuple[int, float]:
    from collections import Counter
    c = Counter(int(s) for s in states)
    mode_state, mode_count = c.most_common(1)[0]
    return mode_state, mode_count / len(states)


def _coordinated_fitness(states: np.ndarray, landscape) -> float:
    mode_state, concentration = _mode_and_concentration(states)
    raw = landscape.fitness_idx(mode_state)
    return raw - FRAGMENTATION_COST * (1.0 - concentration)


def run_horizontal(landscape, tau, n_agents, T, rng, init_state):
    states = np.full(n_agents, init_state, dtype=np.int64)
    perturbations = rng.integers(0, landscape.N, size=n_agents)
    for i, p in enumerate(perturbations):
        if i > 0 and rng.random() < 0.5:
            states[i] ^= (1 << int(p))

    fit_traj = [_coordinated_fitness(states, landscape)]

    for _ in range(T):
        for i in range(n_agents):
            flip = agent_best_flip(int(states[i]), landscape, tau, rng)
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
        fit_traj.append(_coordinated_fitness(states, landscape))
    firm_fit = _coordinated_fitness(states, landscape)
    return states, fit_traj, firm_fit


def run_hybrid(landscape, tau, n_agents, T, rng, init_state,
               cluster_size: int = 5):
    n_clusters = max(1, n_agents // cluster_size)
    leader_states = np.full(n_clusters, init_state, dtype=np.int64)
    for c in range(1, n_clusters):
        if rng.random() < 0.5:
            bit = int(rng.integers(0, landscape.N))
            leader_states[c] ^= (1 << bit)

    fit_traj = [_coordinated_fitness(leader_states, landscape)]

    for _ in range(T):
        for c in range(n_clusters):
            s = int(leader_states[c])
            for _ in range(cluster_size):
                flip = agent_best_flip(s, landscape, tau, rng)
                if flip != -1:
                    candidate = s ^ (1 << flip)
                    if landscape.fitness_idx(candidate) > landscape.fitness_idx(s):
                        s = candidate
            leader_states[c] = s
        if rng.random() < tau:
            ranked = sorted(range(n_clusters),
                            key=lambda i: landscape.fitness_idx(int(leader_states[i])),
                            reverse=True)
            top = int(leader_states[ranked[0]])
            worst = ranked[-1]
            leader_states[worst] = top
        fit_traj.append(_coordinated_fitness(leader_states, landscape))

    return leader_states, fit_traj, fit_traj[-1]


STRUCT_FUNS = {"V": run_vertical, "H": run_horizontal, "Hy": run_hybrid}


def run_single_v2(structure, tau, K, seed, N=15, n_agents=30, T=40):
    rng = np.random.default_rng(seed * 13_001 + K * 37 + int(tau * 100))
    landscape = NKLandscape(N=N, K=K, seed=seed)
    init_state = int(rng.integers(0, 1 << N))
    fit0 = landscape.fitness_idx(init_state)

    fun = STRUCT_FUNS[structure]
    _, traj, final_fit = fun(landscape, tau, n_agents, T, rng, init_state)
    peak = max(traj)
    target = fit0 + 0.95 * (peak - fit0)
    steps_to_95 = T
    for t, f in enumerate(traj):
        if f >= target:
            steps_to_95 = t
            break

    return {
        "structure": structure,
        "tau": tau,
        "K": K,
        "seed": seed,
        "initial_fitness": fit0,
        "final_fitness": final_fit,
        "peak_fitness": peak,
        "improvement": final_fit - fit0,
        "steps_to_95pct": steps_to_95,
        "N": N, "n_agents": n_agents, "T": T,
    }


def run_factorial_v2(out_path,
                     structures=("V", "H", "Hy"),
                     taus=tuple(round(0.1 * i, 2) for i in range(1, 10)),
                     Ks=(2, 5, 10),
                     seeds=range(1, 41),
                     N=15, n_agents=30, T=40):
    cells = [(s, tau, K, seed)
             for s in structures for tau in taus for K in Ks for seed in seeds]
    print(f"v2 total runs: {len(cells)}")

    rows = [run_single_v2(*c, N=N, n_agents=n_agents, T=T) for c in tqdm(cells)]
    df = pd.DataFrame(rows)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    df.to_csv(out_path, index=False)
    print(f"Wrote {out_path}")
    return df


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.normpath(os.path.join(here, "..", "results", "results_v2.csv"))
    df = run_factorial_v2(out)
    print("\nPreview:")
    print(df.groupby(["K", "tau", "structure"])["final_fitness"]
            .mean().unstack("structure").round(3))
