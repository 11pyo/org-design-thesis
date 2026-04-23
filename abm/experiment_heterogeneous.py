"""
Heterogeneous-agent extension (resolves Critique 5).

The practitioner critique: real organizations have enormous variance in
individual competence, not homogeneous agents. The V-wins-under-volatility
finding might actually be "talent-concentration-wins-under-volatility"
with volatility as a proxy for any condition that rewards concentrated
expertise.

We test robustness of H5 under three agent-heterogeneity regimes:

  'homogeneous'    : all agents share tau (baseline)
  'mild'           : tau_i ~ Normal(tau, sigma=0.10), clipped to [0, 1]
  'skewed'         : 20% of agents have 2*tau (capped), rest have 0.5*tau
                     -- models a "few stars, many juniors" distribution
  'extreme'        : 10% of agents have tau=1.0, rest have tau*0.3
                     -- near-total talent concentration

H5 survives if the V-H gap remains positive and monotone in volatility
across all regimes. It dies if the gap disappears when talent is
distributed-uniformly rather than concentrated.

Reference: Bloom, Genakos, Sadun, Van Reenen (2012) on management-practice
dispersion; Azoulay, Graff Zivin, Wang (2010) on star scientists.

Writes results/results_heterogeneous.csv.
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


def make_tau_vector(mode: str, mean_tau: float, n: int, rng: np.random.Generator):
    if mode == "homogeneous":
        return np.full(n, mean_tau)
    if mode == "mild":
        return np.clip(rng.normal(mean_tau, 0.10, size=n), 0.01, 0.99)
    if mode == "skewed":
        taus = np.full(n, mean_tau * 0.5)
        n_stars = max(1, int(round(0.2 * n)))
        stars = rng.choice(n, size=n_stars, replace=False)
        taus[stars] = np.clip(mean_tau * 2.0, 0.01, 0.99)
        return np.clip(taus, 0.01, 0.99)
    if mode == "extreme":
        taus = np.full(n, mean_tau * 0.3)
        n_stars = max(1, int(round(0.1 * n)))
        stars = rng.choice(n, size=n_stars, replace=False)
        taus[stars] = 1.0
        return np.clip(taus, 0.01, 0.99)
    raise ValueError(mode)


def agent_best_flip_with_tau(state_int, landscape, tau_i, rng):
    return v2.agent_best_flip(state_int, landscape, tau_i, rng)


def run_one(heterogeneity, structure, tau, K, seed, shock_every,
            N=15, n_agents=30, T=40):
    rng = np.random.default_rng(hash((heterogeneity, structure, tau, K, seed, shock_every)) & 0xFFFFFFFF)
    landscape = NKLandscape(N=N, K=K, seed=seed)
    init_state = int(rng.integers(0, 1 << N))

    taus = make_tau_vector(heterogeneity, tau, n_agents, rng)

    if structure == "V":
        state = init_state
        ceo_idx = int(np.argmax(taus))
        tau_ceo = min(1.0, taus[ceo_idx] * 1.3)
        for t in range(T):
            if (t + 1) % shock_every == 0:
                ed.shock(landscape, rng)
            best_move = agent_best_flip_with_tau(state, landscape, tau_ceo, rng)
            subord = [agent_best_flip_with_tau(state, landscape, taus[i], rng)
                      for i in range(n_agents) if i != ceo_idx]
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
                flip = agent_best_flip_with_tau(int(states[i]), landscape, taus[i], rng)
                if flip != -1:
                    states[i] ^= (1 << flip)
            for i in range(n_agents):
                avg_tau = (taus[i] + np.mean(taus)) / 2
                if rng.random() < avg_tau:
                    partner = int(rng.integers(0, n_agents))
                    if partner != i:
                        f_i = landscape.fitness_idx(int(states[i]))
                        f_p = landscape.fitness_idx(int(states[partner]))
                        if f_p > f_i:
                            states[i] = states[partner]
        final_fit = v2._coordinated_fitness(states, landscape)
    else:  # Hy
        cluster_size = 5
        n_clusters = max(1, n_agents // cluster_size)
        cluster_membership = np.repeat(np.arange(n_clusters), cluster_size)[:n_agents]
        leader_taus = np.array([taus[cluster_membership == c].max() for c in range(n_clusters)])
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
                    flip = agent_best_flip_with_tau(s, landscape, leader_taus[c], rng)
                    if flip != -1:
                        cand = s ^ (1 << flip)
                        if landscape.fitness_idx(cand) > landscape.fitness_idx(s):
                            s = cand
                leader_states[c] = s
            if rng.random() < float(np.mean(leader_taus)):
                ranked = sorted(range(n_clusters),
                                key=lambda i: landscape.fitness_idx(int(leader_states[i])),
                                reverse=True)
                leader_states[ranked[-1]] = leader_states[ranked[0]]
        final_fit = v2._coordinated_fitness(leader_states, landscape)

    return {"heterogeneity": heterogeneity, "structure": structure,
            "tau": tau, "K": K, "seed": seed,
            "shock_every": shock_every, "final_fitness": final_fit}


def main():
    regimes = ("homogeneous", "mild", "skewed", "extreme")
    shock_levels = [100, 10, 3]
    structures = ("V", "H", "Hy")
    taus = (0.5,)
    Ks = (5,)
    seeds = range(1, 21)

    cells = [(h, s, tau, K, seed, se)
             for h in regimes
             for s in structures
             for tau in taus
             for K in Ks
             for seed in seeds
             for se in shock_levels]
    print(f"total runs: {len(cells)}", flush=True)
    rows = [run_one(*c) for c in tqdm(cells)]
    df = pd.DataFrame(rows)
    out = os.path.normpath(os.path.join(HERE, "..", "results", "results_heterogeneous.csv"))
    df.to_csv(out, index=False)
    print(f"Wrote {out}", flush=True)

    from scipy.stats import spearmanr
    print("\nSpearman rho(shock_freq, V-H) per heterogeneity regime:")
    for h in regimes:
        sub = df[df["heterogeneity"] == h]
        g = sub.groupby(["shock_every", "structure"])["final_fitness"].mean().unstack()
        g["V_minus_H"] = g["V"] - g["H"]
        g["vol"] = 1.0 / g.index
        rho, p = spearmanr(g["vol"], g["V_minus_H"])
        print(f"  {h:15s}: rho = {rho:+.3f}  p = {p:.4g}")


if __name__ == "__main__":
    main()
