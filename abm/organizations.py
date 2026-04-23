"""
Three organization types that aggregate agent proposals into a firm move.

Vertical:
    CEO dominates. Workers/managers submit proposals, CEO picks the
    highest-fitness one (from her direct reports + her own search).
    CEO always executes. High decisiveness, low diversity of views.

Horizontal:
    All peers propose. Firm adopts a move only if at least `consensus_frac`
    of non-null proposals converge on the same bit-flip. Otherwise firm
    stays put. Models coordination cost of flat structures.

Hybrid:
    Members within each cluster (5 agents) pick majority proposal.
    Cluster leaders then vote; firm adopts if >=1/2 of leaders agree.
    Blends decisiveness with local diversity.
"""

from __future__ import annotations
import numpy as np
from collections import Counter

from agents import Agent


def vertical_step(agents: list[Agent], state_int: int, landscape,
                  rng: np.random.Generator) -> int:
    ceo = agents[0]
    managers = [a for a in agents if a.role == "mgr"]
    workers = [a for a in agents if a.role == "worker"]

    ceo_prop = ceo.propose(state_int, landscape, rng)
    worker_by_mgr = np.array_split(workers, max(1, len(managers)))
    mgr_filtered = []
    for mgr, w_group in zip(managers, worker_by_mgr):
        proposals = [mgr.propose(state_int, landscape, rng)]
        for w in w_group:
            proposals.append(w.propose(state_int, landscape, rng))
        best_bit, best_fit = -1, landscape.current_fitness_idx(state_int)
        for p in proposals:
            if p == -1:
                continue
            f = landscape.all_one_bit_flip_fitnesses(state_int)[p]
            if f > best_fit:
                best_bit, best_fit = p, f
        mgr_filtered.append(best_bit)

    candidates = [ceo_prop] + mgr_filtered
    best_bit, best_fit = -1, landscape.current_fitness_idx(state_int)
    for p in candidates:
        if p == -1:
            continue
        f = landscape.all_one_bit_flip_fitnesses(state_int)[p]
        if f > best_fit:
            best_bit, best_fit = p, f

    if best_bit == -1:
        return state_int
    return state_int ^ (1 << best_bit)


def horizontal_step(agents: list[Agent], state_int: int, landscape,
                    rng: np.random.Generator,
                    consensus_frac: float = 0.33) -> int:
    proposals = [a.propose(state_int, landscape, rng) for a in agents]
    non_null = [p for p in proposals if p != -1]

    if not non_null:
        return state_int

    counts = Counter(non_null)
    top_bit, top_count = counts.most_common(1)[0]

    if top_count / len(agents) < consensus_frac:
        return state_int

    return state_int ^ (1 << top_bit)


def hybrid_step(agents: list[Agent], state_int: int, landscape,
                rng: np.random.Generator,
                cluster_size: int = 5) -> int:
    clusters: list[list[Agent]] = []
    buf: list[Agent] = []
    for a in agents:
        if a.role == "leader" and buf:
            clusters.append(buf)
            buf = []
        buf.append(a)
    if buf:
        clusters.append(buf)

    cluster_winners = []
    for cl in clusters:
        proposals = [a.propose(state_int, landscape, rng) for a in cl]
        non_null = [p for p in proposals if p != -1]
        if not non_null:
            cluster_winners.append(-1)
            continue
        counts = Counter(non_null)
        top_bit, top_count = counts.most_common(1)[0]
        if top_count >= max(2, len(cl) // 2):
            cluster_winners.append(top_bit)
        else:
            cluster_winners.append(-1)

    valid = [b for b in cluster_winners if b != -1]
    if not valid:
        return state_int
    counts = Counter(valid)
    top_bit, top_count = counts.most_common(1)[0]
    if top_count < max(1, len(cluster_winners) // 2):
        return state_int
    return state_int ^ (1 << top_bit)


STEP_FUNS = {
    "V": vertical_step,
    "H": horizontal_step,
    "Hy": hybrid_step,
}
